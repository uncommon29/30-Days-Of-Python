"""
Main ETL Pipeline Orchestrator

This script orchestrates the complete ETL (Extract, Transform, Load) pipeline.
It runs all three phases in sequence with proper error handling and logging.
"""

import os
import sys
import logging
import yaml
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from extract import main as run_extraction
from transform import main as run_transformation
from load import main as run_loading


def load_config(config_path="config/config.yaml"):
    """Load configuration from YAML file."""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


def setup_logging(config):
    """Setup logging based on configuration."""
    log_level = getattr(logging, config['logging']['level'])
    log_format = config['logging']['format']
    log_file = config['logging']['log_file']
    
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


def run_pipeline():
    """
    Run the complete ETL pipeline.
    
    Returns:
        bool: True if pipeline completed successfully
    """
    # Load configuration
    config = load_config()
    
    # Setup logging
    logger = setup_logging(config)
    
    # Log pipeline start
    logger.info("=" * 80)
    logger.info("BATCH ETL PIPELINE - STARTED")
    logger.info(f"Start time: {datetime.now().isoformat()}")
    logger.info("=" * 80)
    
    # Track pipeline stages
    stages_completed = []
    stages_failed = []
    start_time = datetime.now()
    
    try:
        # Stage 1: Extract
        logger.info("\n" + "=" * 80)
        logger.info("STAGE 1/3: EXTRACTION")
        logger.info("=" * 80)
        
        extract_start = datetime.now()
        run_extraction()
        extract_end = datetime.now()
        extract_duration = (extract_end - extract_start).total_seconds()
        
        stages_completed.append({
            'stage': 'Extraction',
            'status': 'SUCCESS',
            'duration_seconds': extract_duration,
            'timestamp': extract_end.isoformat()
        })
        
        logger.info(f"\nExtraction completed in {extract_duration:.2f} seconds")
        
        # Stage 2: Transform
        logger.info("\n" + "=" * 80)
        logger.info("STAGE 2/3: TRANSFORMATION")
        logger.info("=" * 80)
        
        transform_start = datetime.now()
        run_transformation()
        transform_end = datetime.now()
        transform_duration = (transform_end - transform_start).total_seconds()
        
        stages_completed.append({
            'stage': 'Transformation',
            'status': 'SUCCESS',
            'duration_seconds': transform_duration,
            'timestamp': transform_end.isoformat()
        })
        
        logger.info(f"\nTransformation completed in {transform_duration:.2f} seconds")
        
        # Stage 3: Load
        logger.info("\n" + "=" * 80)
        logger.info("STAGE 3/3: LOADING")
        logger.info("=" * 80)
        
        load_start = datetime.now()
        run_loading()
        load_end = datetime.now()
        load_duration = (load_end - load_start).total_seconds()
        
        stages_completed.append({
            'stage': 'Loading',
            'status': 'SUCCESS',
            'duration_seconds': load_duration,
            'timestamp': load_end.isoformat()
        })
        
        logger.info(f"\nLoading completed in {load_duration:.2f} seconds")
        
        # Calculate total duration
        end_time = datetime.now()
        total_duration = (end_time - start_time).total_seconds()
        
        # Log pipeline completion
        logger.info("\n" + "=" * 80)
        logger.info("BATCH ETL PIPELINE - COMPLETED SUCCESSFULLY")
        logger.info(f"End time: {end_time.isoformat()}")
        logger.info(f"Total duration: {total_duration:.2f} seconds")
        logger.info("=" * 80)
        
        # Print summary
        logger.info("\n" + "=" * 80)
        logger.info("PIPELINE EXECUTION SUMMARY")
        logger.info("=" * 80)
        
        for stage in stages_completed:
            status_icon = "✓" if stage['status'] == 'SUCCESS' else "✗"
            logger.info(f"{status_icon} {stage['stage']}: {stage['duration_seconds']:.2f}s")
        
        logger.info("=" * 80)
        
        return True
    
    except Exception as e:
        # Log pipeline failure
        logger.error("=" * 80)
        logger.error("BATCH ETL PIPELINE - FAILED")
        logger.error(f"Error: {str(e)}")
        logger.error(f"Failure time: {datetime.now().isoformat()}")
        logger.error("=" * 80)
        
        # Track failed stage
        stages_failed.append({
            'stage': 'Unknown',
            'status': 'FAILED',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        })
        
        return False


def main():
    """Main entry point for the ETL pipeline."""
    print("\n" + "=" * 80)
    print("BATCH ETL PIPELINE")
    print("Processing Iris Dataset")
    print("=" * 80 + "\n")
    
    success = run_pipeline()
    
    if success:
        print("\n" + "=" * 80)
        print("✓ PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 80)
        print("\nOutput files:")
        print("  - data/raw/iris_raw.csv")
        print("  - data/processed/iris_processed.csv")
        print("  - data/output/iris_final.csv")
        print("  - data/output/iris_summary.json")
        print("  - logs/etl_pipeline.log")
        print("\n" + "=" * 80 + "\n")
        sys.exit(0)
    else:
        print("\n" + "=" * 80)
        print("✗ PIPELINE FAILED")
        print("=" * 80)
        print("\nCheck logs/etl_pipeline.log for details")
        print("\n" + "=" * 80 + "\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
