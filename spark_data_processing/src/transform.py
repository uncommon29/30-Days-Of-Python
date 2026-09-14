"""Data transformation module with aggregations, window functions, and data quality checks."""

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import (
    col, count, sum, avg, min, max, date_format, 
    to_date, datediff, lit, rank, dense_rank, row_number,
    lag, lead, when, coalesce, expr, countDistinct
)
from pyspark.sql.window import Window
from pyspark.sql.types import StructType
import os
from datetime import datetime

from spark_session import load_config, get_data_paths


def check_data_quality(df: DataFrame, config: dict) -> dict:
    """
    Perform data quality checks on the DataFrame.
    
    Args:
        df: Input DataFrame
        config: Configuration dictionary
        
    Returns:
        Dictionary with quality check results
    """
    total_records = df.count()
    quality_config = config.get('processing', {}).get('quality', {})
    max_null_pct = quality_config.get('max_null_percentage', 5.0)
    
    results = {
        'total_records': total_records,
        'checks': {},
        'passed': True,
        'timestamp': datetime.now().isoformat()
    }
    
    # Check for nulls in each column
    null_counts = {}
    for column in df.columns:
        null_count = df.filter(col(column).isNull()).count()
        null_pct = (null_count / total_records * 100) if total_records > 0 else 0
        null_counts[column] = {
            'null_count': null_count,
            'null_percentage': round(null_pct, 2)
        }
        
        if null_pct > max_null_pct:
            results['passed'] = False
            results['checks'][f'null_{column}'] = {
                'status': 'FAILED',
                'message': f'Null percentage ({null_pct:.2f}%) exceeds threshold ({max_null_pct}%)'
            }
        else:
            results['checks'][f'null_{column}'] = {
                'status': 'PASSED',
                'message': f'Null percentage ({null_pct:.2f}%) within threshold'
            }
    
    results['null_summary'] = null_counts
    
    # Check for duplicates
    duplicate_count = df.count() - df.dropDuplicates(['transaction_id']).count()
    if duplicate_count > 0:
        results['passed'] = False
        results['checks']['duplicates'] = {
            'status': 'FAILED',
            'message': f'Found {duplicate_count} duplicate transactions'
        }
    else:
        results['checks']['duplicates'] = {
            'status': 'PASSED',
            'message': 'No duplicate transactions found'
        }
    results['duplicate_count'] = duplicate_count
    
    # Check price range
    min_price = quality_config.get('min_price', 0.01)
    max_price = quality_config.get('max_price', 10000.0)
    
    invalid_price_count = df.filter(
        (col('price') < min_price) | (col('price') > max_price)
    ).count()
    
    if invalid_price_count > 0:
        results['passed'] = False
        results['checks']['price_range'] = {
            'status': 'FAILED',
            'message': f'{invalid_price_count} records with invalid prices'
        }
    else:
        results['checks']['price_range'] = {
            'status': 'PASSED',
            'message': 'All prices within valid range'
        }
    
    # Check quantity range
    min_qty = quality_config.get('min_quantity', 1)
    max_qty = quality_config.get('max_quantity', 100)
    
    invalid_qty_count = df.filter(
        (col('quantity') < min_qty) | (col('quantity') > max_qty)
    ).count()
    
    if invalid_qty_count > 0:
        results['passed'] = False
        results['checks']['quantity_range'] = {
            'status': 'FAILED',
            'message': f'{invalid_qty_count} records with invalid quantities'
        }
    else:
        results['checks']['quantity_range'] = {
            'status': 'PASSED',
            'message': 'All quantities within valid range'
        }
    
    return results


def calculate_customer_rfm(df: DataFrame) -> DataFrame:
    """
    Calculate RFM (Recency, Frequency, Monetary) metrics for customers.
    
    Args:
        df: Transaction DataFrame
        
    Returns:
        DataFrame with customer RFM scores
    """
    # Get the reference date (latest transaction date)
    max_date = df.agg(max(col('date'))).first()[0]
    
    # Calculate RFM metrics
    rfm = df.groupBy('customer_id').agg(
        datediff(lit(max_date), max(col('date'))).alias('recency'),
        count('transaction_id').alias('frequency'),
        sum('final_amount').alias('monetary')
    )
    
    # Calculate RFM scores (1-5 scale)
    rfm_scores = rfm.withColumn(
        'r_score',
        when(col('recency') <= 30, 5)
        .when(col('recency') <= 60, 4)
        .when(col('recency') <= 90, 3)
        .when(col('recency') <= 180, 2)
        .otherwise(1)
    ).withColumn(
        'f_score',
        when(col('frequency') >= 10, 5)
        .when(col('frequency') >= 5, 4)
        .when(col('frequency') >= 3, 3)
        .when(col('frequency') >= 2, 2)
        .otherwise(1)
    ).withColumn(
        'm_score',
        when(col('monetary') >= 1000, 5)
        .when(col('monetary') >= 500, 4)
        .when(col('monetary') >= 200, 3)
        .when(col('monetary') >= 100, 2)
        .otherwise(1)
    )
    
    # Calculate combined RFM score
    rfm_scores = rfm_scores.withColumn(
        'rfm_score',
        col('r_score') * 100 + col('f_score') * 10 + col('m_score')
    )
    
    # Assign customer segments
    segments = rfm_scores.withColumn(
        'segment',
        when((col('r_score') >= 4) & (col('f_score') >= 4) & (col('m_score') >= 4), 'Platinum')
        .when((col('r_score') >= 3) & (col('f_score') >= 3) & (col('m_score') >= 3), 'Gold')
        .when((col('r_score') >= 2) & (col('f_score') >= 2) & (col('m_score') >= 2), 'Silver')
        .otherwise('Bronze')
    )
    
    return segments


def calculate_product_performance(df: DataFrame) -> DataFrame:
    """
    Calculate product performance metrics.
    
    Args:
        df: Transaction DataFrame
        
    Returns:
        DataFrame with product performance metrics
    """
    product_perf = df.groupBy('product_id', 'category').agg(
        count('transaction_id').alias('sales_count'),
        sum('quantity').alias('total_quantity'),
        sum('final_amount').alias('total_revenue'),
        avg('final_amount').alias('avg_order_value'),
        avg('discount').alias('avg_discount'),
        countDistinct('customer_id').alias('unique_customers')
    )
    
    # Add rankings
    window_spec = Window.orderBy(col('total_revenue').desc())
    
    product_perf = product_perf.withColumn(
        'revenue_rank',
        rank().over(window_spec)
    ).withColumn(
        'sales_rank',
        rank().over(Window.orderBy(col('sales_count').desc()))
    )
    
    # Category ranking
    category_window = Window.partitionBy('category').orderBy(col('total_revenue').desc())
    product_perf = product_perf.withColumn(
        'category_rank',
        rank().over(category_window)
    )
    
    return product_perf


def calculate_daily_revenue(df: DataFrame, window_days: list = None) -> DataFrame:
    """
    Calculate daily revenue with moving averages.
    
    Args:
        df: Transaction DataFrame
        window_days: List of window sizes for moving averages
        
    Returns:
        DataFrame with daily revenue and moving averages
    """
    if window_days is None:
        window_days = [7, 30]
    
    # Daily aggregation
    daily = df.groupBy('date').agg(
        count('transaction_id').alias('transaction_count'),
        sum('final_amount').alias('daily_revenue'),
        avg('final_amount').alias('avg_transaction_value'),
        countDistinct('customer_id').alias('unique_customers'),
        countDistinct('product_id').alias('unique_products')
    )
    
    # Define window for time-series calculations
    window_spec = Window.orderBy('date')
    
    # Add moving averages
    for days in window_days:
        daily = daily.withColumn(
            f'moving_avg_{days}d',
            avg(col('daily_revenue')).over(
                window_spec.rowsBetween(-(days-1), 0)
            )
        )
    
    # Add running total
    daily = daily.withColumn(
        'running_total_revenue',
        sum(col('daily_revenue')).over(window_spec.rowsBetween(Window.unboundedPreceding, 0))
    )
    
    # Add day-over-day change
    daily = daily.withColumn(
        'prev_day_revenue',
        lag(col('daily_revenue'), 1).over(window_spec)
    ).withColumn(
        'dod_change_pct',
        when(col('prev_day_revenue').isNotNull(),
             ((col('daily_revenue') - col('prev_day_revenue')) / col('prev_day_revenue') * 100)
            ).otherwise(None)
    )
    
    return daily


def calculate_category_analytics(df: DataFrame) -> DataFrame:
    """
    Calculate category-level analytics.
    
    Args:
        df: Transaction DataFrame
        
    Returns:
        DataFrame with category analytics
    """
    category_stats = df.groupBy('category').agg(
        count('transaction_id').alias('transaction_count'),
        sum('final_amount').alias('total_revenue'),
        avg('final_amount').alias('avg_order_value'),
        sum('quantity').alias('total_units_sold'),
        countDistinct('product_id').alias('unique_products'),
        countDistinct('customer_id').alias('unique_customers'),
        avg('discount').alias('avg_discount')
    )
    
    # Calculate revenue share
    total_revenue = category_stats.agg(sum('total_revenue')).first()[0]
    category_stats = category_stats.withColumn(
        'revenue_share_pct',
        (col('total_revenue') / total_revenue * 100) if total_revenue > 0 else lit(0)
    )
    
    # Rank categories
    category_stats = category_stats.withColumn(
        'revenue_rank',
        rank().over(Window.orderBy(col('total_revenue').desc()))
    )
    
    return category_stats


def calculate_region_analytics(df: DataFrame) -> DataFrame:
    """
    Calculate region-level analytics.
    
    Args:
        df: Transaction DataFrame
        
    Returns:
        DataFrame with region analytics
    """
    region_stats = df.groupBy('region').agg(
        count('transaction_id').alias('transaction_count'),
        sum('final_amount').alias('total_revenue'),
        avg('final_amount').alias('avg_order_value'),
        countDistinct('customer_id').alias('unique_customers'),
        countDistinct('product_id').alias('unique_products')
    )
    
    # Rank regions
    region_stats = region_stats.withColumn(
        'revenue_rank',
        rank().over(Window.orderBy(col('total_revenue').desc()))
    )
    
    return region_stats


def transform_data(spark=None, config=None) -> dict:
    """
    Main transformation function that orchestrates all transformations.
    
    Args:
        spark: SparkSession instance
        config: Configuration dictionary
        
    Returns:
        Dictionary with transformed DataFrames and quality report
    """
    if config is None:
        config = load_config()
    
    if spark is None:
        from spark_session import create_spark_session
        spark = create_spark_session(config)
    
    paths = get_data_paths(config)
    raw_path = paths['raw']
    processed_path = paths['processed']
    
    # Load raw data
    print("Loading raw data...")
    raw_df = spark.read.csv(
        os.path.join(raw_path, "transactions_raw.csv"),
        header=True,
        inferSchema=True
    )
    
    # Convert date column properly
    from pyspark.sql.functions import to_date
    raw_df = raw_df.withColumn('date', to_date(col('date'), 'yyyy-MM-dd'))
    
    print(f"Loaded {raw_df.count()} records")
    
    # Data quality check
    print("\nPerforming data quality checks...")
    quality_report = check_data_quality(raw_df, config)
    
    # Transformations
    print("\nCalculating customer RFM...")
    customer_rfm = calculate_customer_rfm(raw_df)
    
    print("Calculating product performance...")
    product_perf = calculate_product_performance(raw_df)
    
    print("Calculating daily revenue...")
    window_days = config.get('processing', {}).get('moving_avg_windows', [7, 30])
    daily_revenue = calculate_daily_revenue(raw_df, window_days)
    
    print("Calculating category analytics...")
    category_analytics = calculate_category_analytics(raw_df)
    
    print("Calculating region analytics...")
    region_analytics = calculate_region_analytics(raw_df)
    
    # Save processed data
    os.makedirs(processed_path, exist_ok=True)
    
    print(f"\nSaving processed data to {processed_path}...")
    
    customer_rfm.write.mode("overwrite").parquet(
        os.path.join(processed_path, "customer_rfm.parquet")
    )
    
    product_perf.write.mode("overwrite").option("header", "true").csv(
        os.path.join(processed_path, "product_performance.csv")
    )
    
    daily_revenue.write.mode("overwrite").option("header", "true").csv(
        os.path.join(processed_path, "daily_revenue.csv")
    )
    
    category_analytics.write.mode("overwrite").option("header", "true").csv(
        os.path.join(processed_path, "category_analytics.csv")
    )
    
    region_analytics.write.mode("overwrite").option("header", "true").csv(
        os.path.join(processed_path, "region_analytics.csv")
    )
    
    print("Transformations complete!")
    
    return {
        'customer_rfm': customer_rfm,
        'product_performance': product_perf,
        'daily_revenue': daily_revenue,
        'category_analytics': category_analytics,
        'region_analytics': region_analytics,
        'quality_report': quality_report
    }


if __name__ == "__main__":
    import logging
    import json
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    config = load_config()
    spark = create_spark_session(config)
    
    try:
        results = transform_data(spark, config)
        
        # Print quality report
        print("\n" + "="*50)
        print("DATA QUALITY REPORT")
        print("="*50)
        print(f"Total Records: {results['quality_report']['total_records']}")
        print(f"Overall Status: {'PASSED' if results['quality_report']['passed'] else 'FAILED'}")
        print(f"Duplicate Count: {results['quality_report']['duplicate_count']}")
        
        print("\nQuality Checks:")
        for check_name, check_result in results['quality_report']['checks'].items():
            status = check_result['status']
            message = check_result['message']
            print(f"  [{status}] {check_name}: {message}")
        
        # Show sample outputs
        print("\n" + "="*50)
        print("CUSTOMER RFM SAMPLE")
        print("="*50)
        results['customer_rfm'].show(10, truncate=False)
        
        print("\n" + "="*50)
        print("PRODUCT PERFORMANCE SAMPLE")
        print("="*50)
        results['product_performance'].show(10, truncate=False)
        
        print("\n" + "="*50)
        print("DAILY REVENUE SAMPLE")
        print("="*50)
        results['daily_revenue'].show(10, truncate=False)
        
    finally:
        spark.stop()
