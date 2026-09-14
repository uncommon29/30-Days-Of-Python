# Cloud Data Warehouse: End-to-End Analytics Pipeline

## Overview
This project demonstrates a modern **Cloud Data Warehouse (CDW)** architecture using a simulated cloud environment. It implements the full ELT (Extract-Load-Transform) pattern, moving data from raw sources through staging to a dimensional model (Star Schema) optimized for analytics.

**Key Concepts:** 
- ELT vs ETL
- Star Schema Modeling (Fact & Dimension tables)
- Slowly Changing Dimensions (SCD Type 2)
- Data Quality & Validation
- Cost Optimization (Partitioning/Clustering simulation)

## Architecture
```
[Raw Data Sources] 
       ↓
[Cloud Storage (Simulated)] → Bronze Layer (Raw)
       ↓
[Staging Area] → Silver Layer (Cleaned)
       ↓
[Data Warehouse] → Gold Layer (Aggregated/Dimensional)
       ↓
[BI / Analytics Tools]
```

## Project Structure
```
cloud_data_warehouse/
├── README.md
├── requirements.txt
├── config/
│   └── settings.yaml        # Warehouse config & mappings
├── src/
│   ├── __init__.py
│   ├── extractor.py         # Extract from APIs/Files
│   ├── loader.py            # Load to Staging/Warehouse
│   ├── transformer.py       # Business logic & SCD handling
│   ├── dw_models.py         # Dimensional models definition
│   └── main.py              # Orchestration script
├── output/                  # Simulated warehouse tables
└── logs/                    # Execution logs
```

## Features
1. **Multi-Source Ingestion**: Simulates pulling from S3/GCS and REST APIs.
2. **Staging Area**: Raw data landing zone with schema inference.
3. **Dimensional Modeling**:
   - `DimCustomer`: Customer attributes with SCD Type 2 history.
   - `DimProduct`: Product hierarchy.
   - `FactSales`: Transactional facts with foreign keys.
4. **Data Quality Gates**: Checks for nulls, referential integrity, and duplicates before loading.
5. **Audit Logging**: Tracks load timestamps, row counts, and status.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
Run the full ELT pipeline:
```bash
cd src
python main.py
```

## Output Tables
The pipeline generates the following "tables" (CSV files acting as warehouse tables):
- `dim_customer.csv`: Customer dimensions with validity dates.
- `dim_product.csv`: Product catalog.
- `fact_sales.csv`: Daily sales facts.
- `audit_log.csv`: Pipeline execution history.

## Learning Outcomes
- Understand the difference between ETL and ELT.
- Learn how to design a Star Schema.
- Implement Slowly Changing Dimensions (SCD Type 2).
- Simulate cloud storage layers (Bronze/Silver/Gold).
