# Spark Data Processing Project

A large-scale data processing project using Apache Spark to analyze e-commerce transaction data. This project demonstrates batch processing, aggregations, window functions, and data quality checks on a simulated retail dataset.

## Project Structure

```
spark_data_processing/
├── data/
│   ├── raw/              # Raw input data
│   ├── processed/        # Intermediate processed data
│   └── output/           # Final output files
├── src/
│   ├── __init__.py
│   ├── spark_session.py  # Spark session configuration
│   ├── extract.py        # Data extraction logic
│   ├── transform.py      # Transformation logic
│   ├── load.py           # Data loading logic
│   └── main.py           # Pipeline orchestrator
├── config/
│   └── settings.yaml     # Configuration file
├── logs/                 # Log files
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Features

- **Scalable Processing**: Uses PySpark for distributed data processing
- **Data Quality Checks**: Validates data completeness and consistency
- **Aggregations**: Customer segmentation, product performance, time-based analysis
- **Window Functions**: Running totals, rankings, moving averages
- **Multiple Output Formats**: Parquet, CSV, and JSON outputs
- **Logging**: Comprehensive logging for monitoring and debugging

## Dataset

Simulated e-commerce transaction data with:
- Transaction ID, Customer ID, Product ID
- Timestamp, Quantity, Price, Discount
- Category, Region, Payment Method
- ~10,000 transactions across multiple categories

## Prerequisites

- Python 3.8+
- Apache Spark 3.x (installed via pip or standalone)
- Java 8+ (required for Spark)
- pip packages: `pyspark`, `pyyaml`, `pandas`

## Installation

```bash
cd spark_data_processing
pip install -r requirements.txt
```

## Usage

### Run the Full Pipeline

```bash
python src/main.py
```

### Run Individual Components

**Extract:**
```bash
python src/extract.py
```

**Transform:**
```bash
python src/transform.py
```

**Load:**
```bash
python src/load.py
```

## Configuration

Edit `config/settings.yaml` to customize:
- Input/output paths
- Processing parameters
- Aggregation windows
- Data quality thresholds

## Output Files

1. **customer_segments.parquet**: Customer segmentation by spending behavior
2. **product_performance.csv**: Product sales rankings and metrics
3. **daily_revenue.json**: Daily revenue trends with moving averages
4. **data_quality_report.txt**: Data quality validation results
5. **summary_stats.json**: Overall dataset statistics

## Key Transformations

### Customer Segmentation
- RFM Analysis (Recency, Frequency, Monetary)
- Customer tiers: Platinum, Gold, Silver, Bronze
- Lifetime value calculation

### Product Analytics
- Sales volume by category
- Revenue contribution
- Return rate analysis
- Top/bottom performers

### Time-Series Analysis
- Daily/weekly/monthly revenue
- Moving averages (7-day, 30-day)
- Peak hours identification
- Seasonal patterns

## Data Quality Checks

- Null value detection
- Duplicate record identification
- Range validation (price > 0, quantity > 0)
- Referential integrity checks
- Timestamp consistency

## Logging

All pipeline activities are logged to `logs/spark_pipeline.log` with:
- INFO level for normal operations
- WARNING for data quality issues
- ERROR for failures

## Example Output

```json
{
  "total_transactions": 10000,
  "total_revenue": 1250000.00,
  "unique_customers": 2500,
  "unique_products": 500,
  "date_range": {
    "start": "2024-01-01",
    "end": "2024-12-31"
  },
  "top_category": "Electronics",
  "avg_order_value": 125.00
}
```

## Troubleshooting

### Spark Memory Issues
Increase Spark driver/executor memory in `spark_session.py`:
```python
.config("spark.driver.memory", "4g")
.config("spark.executor.memory", "4g")
```

### Java Not Found
Ensure Java is installed and JAVA_HOME is set:
```bash
export JAVA_HOME=/path/to/java
```

## License

MIT License

## Author

Generated for Spark Data Processing demonstration.
