"""
Extract Module - Extracts data from source and saves to raw data directory.

This module handles the extraction phase of the ETL pipeline.
It fetches the Iris dataset from sklearn's built-in datasets.
"""

import os
import sys
import logging
import yaml
import pandas as pd
from sklearn.datasets import load_iris

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


def extract_iris_data(logger):
    """
    Extract Iris dataset from sklearn.
    
    Returns:
        pd.DataFrame: DataFrame containing the Iris dataset
    """
    logger.info("Starting data extraction...")
    
    try:
        # Load iris dataset from sklearn
        iris = load_iris()
        
        # Create DataFrame with features
        df = pd.DataFrame(
            data=iris.data,
            columns=['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
        )
        
        # Add target column (species)
        df['species'] = pd.Categorical.from_codes(
            iris.target,
            categories=iris.target_names
        )
        
        # Add original species names for reference
        df['species_id'] = iris.target
        
        logger.info(f"Successfully extracted {len(df)} records with {len(df.columns)} columns")
        logger.info(f"Columns: {list(df.columns)}")
        logger.info(f"Species distribution:\n{df['species'].value_counts()}")
        
        return df
    
    except Exception as e:
        logger.error(f"Error during extraction: {str(e)}")
        raise


def save_raw_data(df, output_path, logger):
    """
    Save extracted data to raw data directory.
    
    Args:
        df: DataFrame to save
        output_path: Path to save the file
        logger: Logger instance
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save to CSV
        df.to_csv(output_path, index=False)
        logger.info(f"Raw data saved to: {output_path}")
        logger.info(f"File size: {os.path.getsize(output_path)} bytes")
        
    except Exception as e:
        logger.error(f"Error saving raw data: {str(e)}")
        raise


def validate_extracted_data(df, logger):
    """
    Validate the extracted data.
    
    Args:
        df: DataFrame to validate
        logger: Logger instance
    
    Returns:
        bool: True if validation passes
    """
    logger.info("Validating extracted data...")
    
    # Check for empty dataframe
    if df.empty:
        logger.error("Extracted data is empty")
        return False
    
    # Check for required columns
    required_columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        logger.error(f"Missing required columns: {missing_columns}")
        return False
    
    # Check for null values
    null_counts = df.isnull().sum()
    if null_counts.any():
        logger.warning(f"Found null values:\n{null_counts[null_counts > 0]}")
    
    # Check data types
    logger.info(f"Data types:\n{df.dtypes}")
    
    logger.info("Data validation passed")
    return True


def main():
    """Main function to run the extraction process."""
    # Load configuration
    config = load_config()
    
    # Setup logging
    logger = setup_logging(config)
    
    logger.info("=" * 60)
    logger.info("EXTRACTION PHASE STARTED")
    logger.info("=" * 60)
    
    try:
        # Extract data
        df = extract_iris_data(logger)
        
        # Validate data
        if not validate_extracted_data(df, logger):
            raise ValueError("Data validation failed")
        
        # Save raw data
        output_path = config['paths']['raw_data']
        save_raw_data(df, output_path, logger)
        
        logger.info("=" * 60)
        logger.info("EXTRACTION PHASE COMPLETED SUCCESSFULLY")
        logger.info("=" * 60)
        
        return df
    
    except Exception as e:
        logger.error(f"Extraction phase failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()
