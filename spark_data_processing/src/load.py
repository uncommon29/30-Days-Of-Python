"""Data loading module for saving processed data to various formats."""

from pyspark.sql import DataFrame
import os
import json
from datetime import datetime

from spark_session import load_config, get_data_paths


def save_to_parquet(df: DataFrame, path: str, mode: str = "overwrite") -> str:
    """
    Save DataFrame to Parquet format.
    
    Args:
        df: DataFrame to save
        path: Output path
        mode: Write mode (overwrite, append, etc.)
        
    Returns:
        Full path to saved file
    """
    df.write.mode(mode).parquet(path)
    return path


def save_to_csv(df: DataFrame, path: str, mode: str = "overwrite", header: bool = True) -> str:
    """
    Save DataFrame to CSV format.
    
    Args:
        df: DataFrame to save
        path: Output path
        mode: Write mode
        header: Whether to include header row
        
    Returns:
        Full path to saved file
    """
    df.write.mode(mode).option("header", str(header).lower()).csv(path)
    return path


def save_to_json(df: DataFrame, path: str, mode: str = "overwrite") -> str:
    """
    Save DataFrame to JSON format.
    
    Args:
        df: DataFrame to save
        path: Output path
        mode: Write mode
        
    Returns:
        Full path to saved file
    """
    df.write.mode(mode).json(path)
    return path


def generate_summary_stats(df_dict: dict, config: dict) -> dict:
    """
    Generate summary statistics from all processed DataFrames.
    
    Args:
        df_dict: Dictionary of DataFrames
        config: Configuration dictionary
        
    Returns:
        Dictionary with summary statistics
    """
    summary = {
        'generated_at': datetime.now().isoformat(),
        'datasets': {}
    }
    
    # Customer RFM stats
    if 'customer_rfm' in df_dict:
        rfm_df = df_dict['customer_rfm']
        total_customers = rfm_df.count()
        segment_counts = rfm_df.groupBy('segment').count().collect()
        
        summary['datasets']['customer_rfm'] = {
            'total_customers': total_customers,
            'segments': {row['segment']: row['count'] for row in segment_counts},
            'avg_recency': float(rfm_df.agg({'recency': 'avg'}).first()[0]),
            'avg_frequency': float(rfm_df.agg({'frequency': 'avg'}).first()[0]),
            'avg_monetary': float(rfm_df.agg({'monetary': 'avg'}).first()[0])
        }
    
    # Product performance stats
    if 'product_performance' in df_dict:
        prod_df = df_dict['product_performance']
        summary['datasets']['product_performance'] = {
            'total_products': prod_df.count(),
            'total_revenue': float(prod_df.agg({'total_revenue': 'sum'}).first()[0]),
            'avg_revenue_per_product': float(prod_df.agg({'total_revenue': 'avg'}).first()[0])
        }
    
    # Daily revenue stats
    if 'daily_revenue' in df_dict:
        daily_df = df_dict['daily_revenue']
        summary['datasets']['daily_revenue'] = {
            'total_days': daily_df.count(),
            'total_revenue': float(daily_df.agg({'running_total_revenue': 'max'}).first()[0]),
            'avg_daily_revenue': float(daily_df.agg({'daily_revenue': 'avg'}).first()[0]),
            'max_daily_revenue': float(daily_df.agg({'daily_revenue': 'max'}).first()[0]),
            'min_daily_revenue': float(daily_df.agg({'daily_revenue': 'min'}).first()[0])
        }
    
    # Category analytics stats
    if 'category_analytics' in df_dict:
        cat_df = df_dict['category_analytics']
        category_list = cat_df.select('category', 'total_revenue', 'revenue_rank').collect()
        summary['datasets']['category_analytics'] = {
            'total_categories': cat_df.count(),
            'categories_by_revenue': [
                {'category': row['category'], 'revenue': float(row['total_revenue']), 'rank': row['revenue_rank']}
                for row in sorted(category_list, key=lambda x: x['revenue_rank'])
            ]
        }
    
    # Region analytics stats
    if 'region_analytics' in df_dict:
        reg_df = df_dict['region_analytics']
        region_list = reg_df.select('region', 'total_revenue', 'revenue_rank').collect()
        summary['datasets']['region_analytics'] = {
            'total_regions': reg_df.count(),
            'regions_by_revenue': [
                {'region': row['region'], 'revenue': float(row['total_revenue']), 'rank': row['revenue_rank']}
                for row in sorted(region_list, key=lambda x: x['revenue_rank'])
            ]
        }
    
    return summary


def save_quality_report(quality_report: dict, output_path: str) -> str:
    """
    Save data quality report to a text file.
    
    Args:
        quality_report: Quality report dictionary
        output_path: Output file path
        
    Returns:
        Full path to saved file
    """
    report_lines = [
        "=" * 60,
        "DATA QUALITY REPORT",
        "=" * 60,
        f"Generated: {quality_report.get('timestamp', 'N/A')}",
        f"Total Records: {quality_report.get('total_records', 0)}",
        f"Duplicate Count: {quality_report.get('duplicate_count', 0)}",
        f"Overall Status: {'PASSED' if quality_report.get('passed', False) else 'FAILED'}",
        "",
        "-" * 60,
        "QUALITY CHECKS",
        "-" * 60,
    ]
    
    for check_name, check_result in quality_report.get('checks', {}).items():
        status = check_result.get('status', 'UNKNOWN')
        message = check_result.get('message', 'No details')
        report_lines.append(f"[{status}] {check_name}: {message}")
    
    report_lines.extend([
        "",
        "-" * 60,
        "NULL VALUE SUMMARY",
        "-" * 60,
    ])
    
    null_summary = quality_report.get('null_summary', {})
    for column, stats in null_summary.items():
        null_count = stats.get('null_count', 0)
        null_pct = stats.get('null_percentage', 0)
        report_lines.append(f"{column}: {null_count} nulls ({null_pct:.2f}%)")
    
    report_lines.append("=" * 60)
    
    # Write to file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write('\n'.join(report_lines))
    
    return output_path


def load_data(spark=None, config=None, transform_results: dict = None) -> dict:
    """
    Main loading function that saves all processed data.
    
    Args:
        spark: SparkSession instance
        config: Configuration dictionary
        transform_results: Results from transformation step
        
    Returns:
        Dictionary with output file paths
    """
    if config is None:
        config = load_config()
    
    paths = get_data_paths(config)
    output_path = paths['output']
    processed_path = paths['processed']
    
    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)
    
    output_files = {}
    
    print("Loading and saving final outputs...")
    
    # If transform results provided, use them; otherwise load from processed files
    if transform_results:
        print("Using transformation results directly...")
        
        # Save customer segments
        customer_file = os.path.join(output_path, "customer_segments.parquet")
        save_to_parquet(transform_results['customer_rfm'], customer_file)
        output_files['customer_segments'] = customer_file
        print(f"  Saved: {customer_file}")
        
        # Save product performance
        product_file = os.path.join(output_path, "product_performance.csv")
        save_to_csv(transform_results['product_performance'], product_file)
        output_files['product_performance'] = product_file
        print(f"  Saved: {product_file}")
        
        # Save daily revenue as JSON (convert to pandas first for better JSON handling)
        daily_file = os.path.join(output_path, "daily_revenue.json")
        daily_pdf = transform_results['daily_revenue'].toPandas()
        daily_pdf.to_json(daily_file, orient='records', date_format='iso', indent=2)
        output_files['daily_revenue'] = daily_file
        print(f"  Saved: {daily_file}")
        
        # Save category analytics
        category_file = os.path.join(output_path, "category_analytics.csv")
        save_to_csv(transform_results['category_analytics'], category_file)
        output_files['category_analytics'] = category_file
        print(f"  Saved: {category_file}")
        
        # Save region analytics
        region_file = os.path.join(output_path, "region_analytics.csv")
        save_to_csv(transform_results['region_analytics'], region_file)
        output_files['region_analytics'] = region_file
        print(f"  Saved: {region_file}")
        
        # Generate and save summary statistics
        summary = generate_summary_stats(transform_results, config)
        summary_file = os.path.join(output_path, "summary_stats.json")
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        output_files['summary_stats'] = summary_file
        print(f"  Saved: {summary_file}")
        
        # Save quality report
        quality_file = os.path.join(output_path, "data_quality_report.txt")
        save_quality_report(transform_results['quality_report'], quality_file)
        output_files['quality_report'] = quality_file
        print(f"  Saved: {quality_file}")
    
    else:
        # Load from processed files and save to output
        print("Loading from processed files...")
        
        # Customer segments
        customer_file_in = os.path.join(processed_path, "customer_rfm.parquet")
        customer_file_out = os.path.join(output_path, "customer_segments.parquet")
        if os.path.exists(customer_file_in):
            df = spark.read.parquet(customer_file_in)
            save_to_parquet(df, customer_file_out)
            output_files['customer_segments'] = customer_file_out
        
        # Product performance
        product_file_in = os.path.join(processed_path, "product_performance.csv")
        product_file_out = os.path.join(output_path, "product_performance.csv")
        if os.path.exists(product_file_in):
            df = spark.read.csv(product_file_in, header=True, inferSchema=True)
            save_to_csv(df, product_file_out)
            output_files['product_performance'] = product_file_out
        
        # Daily revenue
        daily_file_in = os.path.join(processed_path, "daily_revenue.csv")
        daily_file_out = os.path.join(output_path, "daily_revenue.json")
        if os.path.exists(daily_file_in):
            df = spark.read.csv(daily_file_in, header=True, inferSchema=True)
            pdf = df.toPandas()
            pdf.to_json(daily_file_out, orient='records', date_format='iso', indent=2)
            output_files['daily_revenue'] = daily_file_out
    
    print("\nLoad complete!")
    print(f"\nOutput files saved to: {output_path}")
    for name, path in output_files.items():
        print(f"  - {name}: {path}")
    
    return output_files


if __name__ == "__main__":
    import logging
    from spark_session import create_spark_session
    from transform import transform_data
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    config = load_config()
    spark = create_spark_session(config)
    
    try:
        # First run transformations
        print("Running transformations...")
        transform_results = transform_data(spark, config)
        
        # Then load/save outputs
        print("\nRunning load step...")
        output_files = load_data(spark, config, transform_results)
        
        print("\n" + "="*50)
        print("PIPELINE COMPLETE")
        print("="*50)
        print(f"\nAll outputs saved to: {get_data_paths(config)['output']}")
        
    finally:
        spark.stop()
