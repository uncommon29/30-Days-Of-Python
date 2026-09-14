"""
Load Module - Loads processed data and exports to final output formats.

This module handles the loading phase of the ETL pipeline.
It creates summary statistics, aggregates data, and exports to multiple formats.
"""

import os
import sys
import logging
import yaml
import json
import pandas as pd
import numpy as np
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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


def load_processed_data(input_path, logger):
    """
    Load processed data from CSV file.
    
    Args:
        input_path: Path to processed data file
        logger: Logger instance
    
    Returns:
        pd.DataFrame: Loaded DataFrame
    """
    logger.info(f"Loading processed data from: {input_path}")
    
    try:
        df = pd.read_csv(input_path)
        logger.info(f"Successfully loaded {len(df)} records with {len(df.columns)} columns")
        return df
    
    except Exception as e:
        logger.error(f"Error loading processed data: {str(e)}")
        raise


def create_summary_statistics(df, group_by_column, logger):
    """
    Create summary statistics grouped by specified column.
    
    Args:
        df: Input DataFrame
        group_by_column: Column to group by
        logger: Logger instance
    
    Returns:
        dict: Summary statistics
    """
    logger.info(f"Creating summary statistics grouped by '{group_by_column}'")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    # Group by specified column
    grouped = df.groupby(group_by_column)
    
    summary = {
        'generated_at': datetime.now().isoformat(),
        'total_records': len(df),
        'groups': {}
    }
    
    for name, group in grouped:
        group_summary = {
            'count': len(group),
            'statistics': {}
        }
        
        for col in numeric_cols:
            group_summary['statistics'][col] = {
                'mean': float(group[col].mean()),
                'std': float(group[col].std()),
                'min': float(group[col].min()),
                'max': float(group[col].max()),
                'median': float(group[col].median())
            }
        
        summary['groups'][str(name)] = group_summary
        logger.info(f"Summary for group '{name}': {len(group)} records")
    
    # Overall statistics
    summary['overall_statistics'] = {}
    for col in numeric_cols:
        summary['overall_statistics'][col] = {
            'mean': float(df[col].mean()),
            'std': float(df[col].std()),
            'min': float(df[col].min()),
            'max': float(df[col].max()),
            'median': float(df[col].median())
        }
    
    return summary


def aggregate_data(df, group_by_column, logger):
    """
    Aggregate data by specified column.
    
    Args:
        df: Input DataFrame
        group_by_column: Column to group by
        logger: Logger instance
    
    Returns:
        pd.DataFrame: Aggregated DataFrame
    """
    logger.info(f"Aggregating data by '{group_by_column}'")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    # Create aggregation dictionary
    agg_dict = {col: ['mean', 'std', 'min', 'max', 'count'] for col in numeric_cols}
    
    # Aggregate
    aggregated = df.groupby(group_by_column).agg(agg_dict)
    
    # Flatten column names
    aggregated.columns = [f'{col}_{stat}' for col, stat in aggregated.columns]
    
    # Reset index to make group_by_column a regular column
    aggregated = aggregated.reset_index()
    
    logger.info(f"Aggregated data shape: {aggregated.shape}")
    
    return aggregated


def export_to_csv(df, output_path, logger):
    """
    Export DataFrame to CSV file.
    
    Args:
        df: DataFrame to export
        output_path: Path to save the file
        logger: Logger instance
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save to CSV
        df.to_csv(output_path, index=False)
        logger.info(f"Data exported to CSV: {output_path}")
        logger.info(f"File size: {os.path.getsize(output_path)} bytes")
        
    except Exception as e:
        logger.error(f"Error exporting to CSV: {str(e)}")
        raise


def export_to_json(data, output_path, logger):
    """
    Export data to JSON file.
    
    Args:
        data: Data to export (dict or DataFrame)
        output_path: Path to save the file
        logger: Logger instance
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Convert DataFrame to dict if necessary
        if isinstance(data, pd.DataFrame):
            data = data.to_dict(orient='records')
        
        # Save to JSON with pretty formatting
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Data exported to JSON: {output_path}")
        logger.info(f"File size: {os.path.getsize(output_path)} bytes")
        
    except Exception as e:
        logger.error(f"Error exporting to JSON: {str(e)}")
        raise


def validate_loaded_data(df, logger):
    """
    Validate the loaded/final data.
    
    Args:
        df: DataFrame to validate
        logger: Logger instance
    
    Returns:
        bool: True if validation passes
    """
    logger.info("Validating final data...")
    
    # Check for empty dataframe
    if df.empty:
        logger.error("Final data is empty")
        return False
    
    # Check for required columns (at least some basic ones)
    required_columns = ['sepal_length', 'petal_length', 'species']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        logger.warning(f"Missing expected columns: {missing_columns}")
    
    # Check for null values
    null_counts = df.isnull().sum()
    if null_counts.any():
        logger.warning(f"Found null values:\n{null_counts[null_counts > 0]}")
    
    # Log final statistics
    logger.info(f"Final DataFrame shape: {df.shape}")
    logger.info(f"Final columns: {list(df.columns)}")
    
    logger.info("Final data validation passed")
    return True


def main():
    """Main function to run the loading process."""
    # Load configuration
    config = load_config()
    
    # Setup logging
    logger = setup_logging(config)
    
    logger.info("=" * 60)
    logger.info("LOADING PHASE STARTED")
    logger.info("=" * 60)
    
    try:
        # Load processed data
        input_path = config['paths']['processed_data']
        df = load_processed_data(input_path, logger)
        
        # Get load configuration
        load_config_section = config['load']
        group_by_column = load_config_section['summary_group_by']
        output_formats = load_config_section['formats']
        
        # Create summary statistics
        summary_stats = create_summary_statistics(df, group_by_column, logger)
        
        # Aggregate data
        aggregated_df = aggregate_data(df, group_by_column, logger)
        
        # Export based on configured formats
        output_csv = config['paths']['output_csv']
        output_json = config['paths']['output_json']
        
        if 'csv' in output_formats:
            export_to_csv(df, output_csv, logger)
        
        if 'json' in output_formats:
            # Export summary statistics to JSON
            export_to_json(summary_stats, output_json, logger)
            
            # Also export aggregated data to a separate JSON file
            aggregated_json_path = output_json.replace('.json', '_aggregated.json')
            export_to_json(aggregated_df, aggregated_json_path, logger)
        
        # Validate final data
        if not validate_loaded_data(df, logger):
            raise ValueError("Final data validation failed")
        
        logger.info("=" * 60)
        logger.info("LOADING PHASE COMPLETED SUCCESSFULLY")
        logger.info("=" * 60)
        
        # Print final summary
        logger.info("\n" + "=" * 60)
        logger.info("FINAL SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Total records processed: {len(df)}")
        logger.info(f"Total features: {len(df.columns)}")
        logger.info(f"Output files created:")
        logger.info(f"  - {output_csv}")
        logger.info(f"  - {output_json}")
        logger.info(f"  - {output_json.replace('.json', '_aggregated.json')}")
        logger.info("=" * 60)
        
        return df
    
    except Exception as e:
        logger.error(f"Loading phase failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()
