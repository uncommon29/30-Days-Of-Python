"""
Transform Module - Transforms raw data through cleaning and feature engineering.

This module handles the transformation phase of the ETL pipeline.
It performs data cleaning, feature engineering, normalization, and encoding.
"""

import os
import sys
import logging
import yaml
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

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


def load_raw_data(input_path, logger):
    """
    Load raw data from CSV file.
    
    Args:
        input_path: Path to raw data file
        logger: Logger instance
    
    Returns:
        pd.DataFrame: Loaded DataFrame
    """
    logger.info(f"Loading raw data from: {input_path}")
    
    try:
        df = pd.read_csv(input_path)
        logger.info(f"Successfully loaded {len(df)} records with {len(df.columns)} columns")
        return df
    
    except Exception as e:
        logger.error(f"Error loading raw data: {str(e)}")
        raise


def handle_missing_values(df, strategy, logger):
    """
    Handle missing values in the dataframe.
    
    Args:
        df: Input DataFrame
        strategy: Strategy to handle missing values ('mean', 'median', 'drop')
        logger: Logger instance
    
    Returns:
        pd.DataFrame: DataFrame with handled missing values
    """
    logger.info(f"Handling missing values with strategy: {strategy}")
    
    null_counts_before = df.isnull().sum().sum()
    
    if null_counts_before == 0:
        logger.info("No missing values found")
        return df
    
    logger.warning(f"Found {null_counts_before} missing values")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if strategy == 'mean':
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    elif strategy == 'median':
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    elif strategy == 'drop':
        df = df.dropna()
    else:
        logger.warning(f"Unknown strategy '{strategy}', using mean")
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    
    null_counts_after = df.isnull().sum().sum()
    logger.info(f"Missing values after handling: {null_counts_after}")
    
    return df


def create_derived_features(df, logger):
    """
    Create derived features from existing columns.
    
    Args:
        df: Input DataFrame
        logger: Logger instance
    
    Returns:
        pd.DataFrame: DataFrame with new features
    """
    logger.info("Creating derived features...")
    
    # Petal ratio (length / width)
    df['petal_ratio'] = df['petal_length'] / df['petal_width']
    logger.info("Created 'petal_ratio' feature")
    
    # Sepal area (length * width)
    df['sepal_area'] = df['sepal_length'] * df['sepal_width']
    logger.info("Created 'sepal_area' feature")
    
    # Petal area (approximate as ellipse)
    df['petal_area'] = np.pi * (df['petal_length'] / 2) * (df['petal_width'] / 2)
    logger.info("Created 'petal_area' feature")
    
    # Sepal to petal length ratio
    df['sepal_petal_ratio'] = df['sepal_length'] / df['petal_length']
    logger.info("Created 'sepal_petal_ratio' feature")
    
    return df


def normalize_columns(df, columns, logger):
    """
    Normalize specified columns using StandardScaler.
    
    Args:
        df: Input DataFrame
        columns: List of columns to normalize
        logger: Logger instance
    
    Returns:
        pd.DataFrame: DataFrame with normalized columns
    """
    logger.info(f"Normalizing columns: {columns}")
    
    scaler = StandardScaler()
    
    for col in columns:
        if col in df.columns:
            df[f'{col}_normalized'] = scaler.fit_transform(df[[col]])
            logger.info(f"Normalized column: {col}")
        else:
            logger.warning(f"Column '{col}' not found, skipping normalization")
    
    return df


def encode_categorical(df, column, method, logger):
    """
    Encode categorical variables.
    
    Args:
        df: Input DataFrame
        column: Column to encode
        method: Encoding method ('label' or 'onehot')
        logger: Logger instance
    
    Returns:
        pd.DataFrame: DataFrame with encoded columns
    """
    logger.info(f"Encoding categorical column '{column}' with method '{method}'")
    
    if column not in df.columns:
        logger.error(f"Column '{column}' not found in DataFrame")
        return df
    
    if method == 'label':
        le = LabelEncoder()
        df[f'{column}_encoded'] = le.fit_transform(df[column])
        logger.info(f"Label encoded '{column}' -> '{column}_encoded'")
        logger.info(f"Encoding mapping: {dict(zip(le.classes_, range(len(le.classes_))))}")
    
    elif method == 'onehot':
        onehot = pd.get_dummies(df[column], prefix=column)
        df = pd.concat([df, onehot], axis=1)
        logger.info(f"One-hot encoded '{column}' into {len(onehot.columns)} columns")
    
    else:
        logger.warning(f"Unknown encoding method '{method}', using label encoding")
        le = LabelEncoder()
        df[f'{column}_encoded'] = le.fit_transform(df[column])
    
    return df


def validate_transformed_data(df, logger):
    """
    Validate the transformed data.
    
    Args:
        df: DataFrame to validate
        logger: Logger instance
    
    Returns:
        bool: True if validation passes
    """
    logger.info("Validating transformed data...")
    
    # Check for empty dataframe
    if df.empty:
        logger.error("Transformed data is empty")
        return False
    
    # Check for infinite values
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    inf_count = np.isinf(df[numeric_cols]).sum().sum()
    if inf_count > 0:
        logger.error(f"Found {inf_count} infinite values")
        return False
    
    # Check for NaN values
    nan_count = df.isnull().sum().sum()
    if nan_count > 0:
        logger.warning(f"Found {nan_count} NaN values")
    
    # Log summary statistics
    logger.info(f"DataFrame shape: {df.shape}")
    logger.info(f"Columns: {list(df.columns)}")
    logger.info(f"Numeric columns summary:\n{df[numeric_cols].describe()}")
    
    logger.info("Data validation passed")
    return True


def save_processed_data(df, output_path, logger):
    """
    Save processed data to file.
    
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
        logger.info(f"Processed data saved to: {output_path}")
        logger.info(f"File size: {os.path.getsize(output_path)} bytes")
        
    except Exception as e:
        logger.error(f"Error saving processed data: {str(e)}")
        raise


def main():
    """Main function to run the transformation process."""
    # Load configuration
    config = load_config()
    
    # Setup logging
    logger = setup_logging(config)
    
    logger.info("=" * 60)
    logger.info("TRANSFORMATION PHASE STARTED")
    logger.info("=" * 60)
    
    try:
        # Load raw data
        input_path = config['paths']['raw_data']
        df = load_raw_data(input_path, logger)
        
        # Store original record count
        original_count = len(df)
        logger.info(f"Original record count: {original_count}")
        
        # Handle missing values
        missing_strategy = config['transformation']['handle_missing']['strategy']
        df = handle_missing_values(df, missing_strategy, logger)
        
        # Create derived features
        df = create_derived_features(df, logger)
        
        # Normalize columns
        normalize_cols = config['transformation']['normalize_columns']
        df = normalize_columns(df, normalize_cols, logger)
        
        # Encode categorical variables
        encode_config = config['transformation']['encode_categorical']
        df = encode_categorical(
            df,
            encode_config['column'],
            encode_config['method'],
            logger
        )
        
        # Validate transformed data
        if not validate_transformed_data(df, logger):
            raise ValueError("Data validation failed")
        
        # Save processed data
        output_path = config['paths']['processed_data']
        save_processed_data(df, output_path, logger)
        
        logger.info(f"Final record count: {len(df)}")
        logger.info(f"Records lost during transformation: {original_count - len(df)}")
        
        logger.info("=" * 60)
        logger.info("TRANSFORMATION PHASE COMPLETED SUCCESSFULLY")
        logger.info("=" * 60)
        
        return df
    
    except Exception as e:
        logger.error(f"Transformation phase failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()
