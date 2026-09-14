"""Data extraction module for generating and loading e-commerce transaction data."""

from pyspark.sql import DataFrame
from pyspark.sql.types import (
    StructType, StructField, IntegerType, StringType, 
    DoubleType, TimestampType, DateType
)
from pyspark.sql.functions import col, expr, lit, current_timestamp
from datetime import datetime, timedelta
import random
import os

from spark_session import create_spark_session, load_config, get_data_paths


def generate_transaction_data(
    spark,
    num_records: int = 10000,
    seed: int = 42,
    categories: list = None,
    regions: list = None,
    payment_methods: list = None
) -> DataFrame:
    """
    Generate simulated e-commerce transaction data.
    
    Args:
        spark: SparkSession instance
        num_records: Number of records to generate
        seed: Random seed for reproducibility
        categories: List of product categories
        regions: List of regions
        payment_methods: List of payment methods
        
    Returns:
        DataFrame with transaction data
    """
    random.seed(seed)
    
    if categories is None:
        categories = [
            'Electronics', 'Clothing', 'Home & Garden', 'Sports & Outdoors',
            'Books', 'Beauty & Health', 'Toys & Games', 'Food & Beverages'
        ]
    
    if regions is None:
        regions = ['North', 'South', 'East', 'West', 'Central']
    
    if payment_methods is None:
        payment_methods = [
            'Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer', 'Cash on Delivery'
        ]
    
    # Generate data
    data = []
    base_date = datetime(2024, 1, 1)
    
    for i in range(num_records):
        transaction_id = f"TXN{i+1:06d}"
        customer_id = f"CUST{random.randint(1, 2500):05d}"
        product_id = f"PROD{random.randint(1, 500):04d}"
        
        # Random timestamp within 2024
        days_offset = random.randint(0, 364)
        hours_offset = random.randint(0, 23)
        minutes_offset = random.randint(0, 59)
        timestamp = base_date + timedelta(
            days=days_offset,
            hours=hours_offset,
            minutes=minutes_offset
        )
        
        quantity = random.randint(1, 10)
        price = round(random.uniform(10.0, 500.0), 2)
        discount = round(random.uniform(0.0, 0.3), 2)  # 0-30% discount
        category = random.choice(categories)
        region = random.choice(regions)
        payment_method = random.choice(payment_methods)
        
        # Calculate final amount
        final_amount = round(quantity * price * (1 - discount), 2)
        
        data.append((
            transaction_id,
            customer_id,
            product_id,
            timestamp,
            timestamp.date(),
            quantity,
            price,
            discount,
            final_amount,
            category,
            region,
            payment_method
        ))
    
    # Define schema
    schema = StructType([
        StructField("transaction_id", StringType(), False),
        StructField("customer_id", StringType(), False),
        StructField("product_id", StringType(), False),
        StructField("timestamp", TimestampType(), False),
        StructField("date", DateType(), False),
        StructField("quantity", IntegerType(), False),
        StructField("price", DoubleType(), False),
        StructField("discount", DoubleType(), False),
        StructField("final_amount", DoubleType(), False),
        StructField("category", StringType(), False),
        StructField("region", StringType(), False),
        StructField("payment_method", StringType(), False)
    ])
    
    # Create DataFrame
    df = spark.createDataFrame(data, schema=schema)
    
    return df


def extract_raw_data(spark=None, config=None) -> DataFrame:
    """
    Extract raw transaction data.
    
    Args:
        spark: SparkSession instance (creates new if None)
        config: Configuration dictionary (loads from file if None)
        
    Returns:
        DataFrame with raw transaction data
    """
    if config is None:
        config = load_config()
    
    if spark is None:
        spark = create_spark_session(config)
    
    data_config = config.get('data', {})
    num_records = data_config.get('num_records', 10000)
    seed = data_config.get('seed', 42)
    
    categories = config.get('categories', None)
    regions = config.get('regions', None)
    payment_methods = config.get('payment_methods', None)
    
    print(f"Generating {num_records} transaction records...")
    df = generate_transaction_data(
        spark=spark,
        num_records=num_records,
        seed=seed,
        categories=categories,
        regions=regions,
        payment_methods=payment_methods
    )
    
    # Save raw data
    paths = get_data_paths(config)
    raw_path = paths['raw']
    
    # Ensure directory exists
    os.makedirs(raw_path, exist_ok=True)
    
    # Save as CSV
    output_file = os.path.join(raw_path, "transactions_raw.csv")
    df.write.mode("overwrite").option("header", "true").csv(output_file)
    print(f"Raw data saved to: {output_file}")
    
    return df


if __name__ == "__main__":
    import logging
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    config = load_config()
    spark = create_spark_session(config)
    
    try:
        df = extract_raw_data(spark, config)
        print(f"\nExtracted {df.count()} records")
        df.printSchema()
        df.show(5, truncate=False)
    finally:
        spark.stop()
