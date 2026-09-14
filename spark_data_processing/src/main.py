"""Main pipeline orchestrator for Spark Data Processing."""

import os
import sys
import logging
from datetime import datetime
from typing import Optional

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from spark_session import create_spark_session, load_config, get_data_paths
from extract import extract_raw_data
from transform import transform_data
from load import load_data


def setup_logging(config: dict) -> logging.Logger:
    """
    Setup logging configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Configured logger instance
    """
    log_config = config.get('logging', {})
    log_level = getattr(logging, log_config.get('level', 'INFO'))
    log_file = log_config.get('file', 'logs/spark_pipeline.log')
    log_format = log_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Get base directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file_path = os.path.join(base_dir, log_file)
    
    # Ensure log directory exists
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger('SparkETLPipeline')


def run_pipeline(config: Optional[dict] = None, full: bool = True) -> dict:
    """
    Run the complete ETL pipeline or individual stages.
    
    Args:
        config: Configuration dictionary (loads from file if None)
        full: If True, runs all stages; if False, runs only specified stages
        
    Returns:
        Dictionary with pipeline results and metrics
    """
    start_time = datetime.now()
    
    # Load configuration
    if config is None:
        config = load_config()
    
    # Setup logging
    logger = setup_logging(config)
    logger.info("="*60)
    logger.info("SPARK DATA PROCESSING PIPELINE")
    logger.info("="*60)
    logger.info(f"Start time: {start_time.isoformat()}")
    logger.info(f"Configuration loaded successfully")
    
    results = {
        'status': 'RUNNING',
        'start_time': start_time.isoformat(),
        'stages': {},
        'metrics': {}
    }
    
    spark = None
    
    try:
        # Initialize Spark session
        logger.info("\nInitializing Spark session...")
        spark = create_spark_session(config)
        logger.info(f"Spark session created: {spark.sparkContext.appName}")
        logger.info(f"Spark version: {spark.version}")
        
        # Stage 1: Extract
        logger.info("\n" + "="*60)
        logger.info("STAGE 1: EXTRACT")
        logger.info("="*60)
        extract_start = datetime.now()
        
        raw_df = extract_raw_data(spark, config)
        record_count = raw_df.count()
        
        extract_end = datetime.now()
        results['stages']['extract'] = {
            'status': 'SUCCESS',
            'start_time': extract_start.isoformat(),
            'end_time': extract_end.isoformat(),
            'duration_seconds': (extract_end - extract_start).total_seconds(),
            'records_extracted': record_count
        }
        logger.info(f"Extract completed: {record_count} records in {(extract_end - extract_start).total_seconds():.2f}s")
        
        # Stage 2: Transform
        logger.info("\n" + "="*60)
        logger.info("STAGE 2: TRANSFORM")
        logger.info("="*60)
        transform_start = datetime.now()
        
        transform_results = transform_data(spark, config)
        
        transform_end = datetime.now()
        results['stages']['transform'] = {
            'status': 'SUCCESS',
            'start_time': transform_start.isoformat(),
            'end_time': transform_end.isoformat(),
            'duration_seconds': (transform_end - transform_start).total_seconds(),
            'quality_passed': transform_results['quality_report']['passed'],
            'outputs_generated': [
                'customer_rfm',
                'product_performance',
                'daily_revenue',
                'category_analytics',
                'region_analytics'
            ]
        }
        logger.info(f"Transform completed in {(transform_end - transform_start).total_seconds():.2f}s")
        logger.info(f"Data quality check: {'PASSED' if transform_results['quality_report']['passed'] else 'FAILED'}")
        
        # Stage 3: Load
        logger.info("\n" + "="*60)
        logger.info("STAGE 3: LOAD")
        logger.info("="*60)
        load_start = datetime.now()
        
        output_files = load_data(spark, config, transform_results)
        
        load_end = datetime.now()
        results['stages']['load'] = {
            'status': 'SUCCESS',
            'start_time': load_start.isoformat(),
            'end_time': load_end.isoformat(),
            'duration_seconds': (load_end - load_start).total_seconds(),
            'output_files': output_files
        }
        logger.info(f"Load completed in {(load_end - load_start).total_seconds():.2f}s")
        logger.info(f"Output files generated: {len(output_files)}")
        
        # Pipeline complete
        end_time = datetime.now()
        total_duration = (end_time - start_time).total_seconds()
        
        results['status'] = 'SUCCESS'
        results['end_time'] = end_time.isoformat()
        results['metrics'] = {
            'total_duration_seconds': total_duration,
            'total_records_processed': record_count,
            'stages_completed': len(results['stages']),
            'output_files_count': len(output_files)
        }
        
        logger.info("\n" + "="*60)
        logger.info("PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("="*60)
        logger.info(f"Total duration: {total_duration:.2f} seconds")
        logger.info(f"Records processed: {record_count}")
        logger.info(f"Output files: {len(output_files)}")
        
        # Print summary
        paths = get_data_paths(config)
        logger.info(f"\nOutput directory: {paths['output']}")
        logger.info("\nGenerated files:")
        for name, path in output_files.items():
            logger.info(f"  - {name}: {path}")
        
    except Exception as e:
        logger.error(f"\nPipeline failed with error: {str(e)}", exc_info=True)
        results['status'] = 'FAILED'
        results['error'] = str(e)
        results['end_time'] = datetime.now().isoformat()
        raise
        
    finally:
        if spark:
            spark.stop()
            logger.info("Spark session stopped")
    
    return results


def main():
    """Main entry point for the pipeline."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Spark Data Processing Pipeline')
    parser.add_argument(
        '--config',
        type=str,
        default=None,
        help='Path to configuration file (default: config/settings.yaml)'
    )
    parser.add_argument(
        '--stage',
        type=str,
        choices=['extract', 'transform', 'load', 'all'],
        default='all',
        help='Pipeline stage to run (default: all)'
    )
    
    args = parser.parse_args()
    
    # Load config
    if args.config:
        config = load_config(args.config)
    else:
        config = load_config()
    
    # Run pipeline
    if args.stage == 'all':
        results = run_pipeline(config, full=True)
    else:
        # For individual stages, you would implement separate logic
        # For now, run full pipeline
        print(f"Running full pipeline (individual stage execution not yet implemented)")
        results = run_pipeline(config, full=True)
    
    # Print final status
    print("\n" + "="*60)
    print("FINAL STATUS")
    print("="*60)
    print(f"Status: {results['status']}")
    if results['status'] == 'SUCCESS':
        print(f"Duration: {results['metrics']['total_duration_seconds']:.2f} seconds")
        print(f"Records: {results['metrics']['total_records_processed']}")
        print(f"Output files: {results['metrics']['output_files_count']}")
    else:
        print(f"Error: {results.get('error', 'Unknown error')}")
    
    return 0 if results['status'] == 'SUCCESS' else 1


if __name__ == "__main__":
    sys.exit(main())
