"""Spark session configuration module."""

from pyspark.sql import SparkSession
from typing import Optional
import yaml
import os


def load_config(config_path: str = "config/settings.yaml") -> dict:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def create_spark_session(config: Optional[dict] = None) -> SparkSession:
    """
    Create and configure a Spark session.
    
    Args:
        config: Configuration dictionary. If None, loads from config/settings.yaml
        
    Returns:
        Configured SparkSession instance
    """
    if config is None:
        config = load_config()
    
    spark_config = config.get('spark', {})
    
    # Build Spark session with configurations
    builder = (SparkSession.builder
             .appName(spark_config.get('app_name', 'EcommerceDataProcessing'))
             .master(spark_config.get('master', 'local[*]'))
             .config("spark.driver.memory", spark_config.get('driver_memory', '2g'))
             .config("spark.executor.memory", spark_config.get('executor_memory', '2g'))
             .config("spark.sql.shuffle.partitions", spark_config.get('sql_shuffle_partitions', 200))
             .config("spark.sql.adaptive.enabled", 
                    str(spark_config.get('sql_adaptive_enabled', True)).lower())
             .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
             .config("spark.sql.adaptive.skewJoin.enabled", "true")
             )
    
    spark = builder.getOrCreate()
    
    # Additional optimizations after session is created
    spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
    spark.conf.set("spark.sql.codegen.wholeStage", "true")
    
    return spark


def get_base_dir() -> str:
    """Get the base directory of the project."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_data_paths(config: dict) -> dict:
    """
    Get absolute paths for data directories.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Dictionary with raw, processed, and output paths
    """
    base_dir = get_base_dir()
    data_config = config.get('data', {})
    
    return {
        'raw': os.path.join(base_dir, data_config.get('raw_path', 'data/raw')),
        'processed': os.path.join(base_dir, data_config.get('processed_path', 'data/processed')),
        'output': os.path.join(base_dir, data_config.get('output_path', 'data/output'))
    }
