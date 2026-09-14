# Complete Guide to Data Engineering Projects
## Concepts, Architectures, and Best Practices

This document explains the core concepts demonstrated across the four data engineering projects in this repository.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Batch ETL Pipeline](#1-batch-etl-pipeline)
3. [Real-time Kafka Pipeline](#2-real-time-kafka-pipeline)
4. [Spark Data Processing](#3-spark-data-processing)
5. [Cloud Data Warehouse](#4-cloud-data-warehouse)
6. [Comparison & When to Use Each](#comparison--when-to-use-each)
7. [Key Data Engineering Concepts](#key-data-engineering-concepts)

---

## Project Overview

| Project | Pattern | Technology | Use Case | Latency |
|---------|---------|------------|----------|---------|
| **Batch ETL** | Extract→Transform→Load | Pandas, Python | Daily reports, historical analysis | Hours/Days |
| **Kafka Streaming** | Event Stream Processing | Apache Kafka | Real-time alerts, monitoring | Milliseconds/Seconds |
| **Spark Processing** | Large-scale Batch | Apache Spark | Big data analytics, ML features | Minutes/Hours |
| **Cloud DW** | ELT (Extract→Load→Transform) | Dimensional Modeling | Business Intelligence, Analytics | Hours |

---

## 1. Batch ETL Pipeline

### What is Batch ETL?
**ETL (Extract, Transform, Load)** is the traditional pattern where data is:
1. **Extracted** from source systems
2. **Transformed** (cleaned, enriched, aggregated) in a staging area
3. **Loaded** into a target database or data warehouse

### Architecture
```
[Source Systems] → [Extraction] → [Transformation Engine] → [Loading] → [Target]
     (CSV/API)         (Python)        (Pandas/Numpy)         (CSV/DB)    (Data Mart)
```

### Key Concepts Learned

#### A. Extraction Strategies
- **Full Load**: Extract all data every time (simple but inefficient)
- **Incremental Load**: Extract only new/changed data (requires tracking)
- **Change Data Capture (CDC)**: Track changes at the source level

#### B. Transformation Types
```python
# 1. Cleaning
df = df.drop_duplicates()
df = df.fillna(value)

# 2. Standardization
df['email'] = df['email'].str.lower().strip()

# 3. Enrichment
df['ratio'] = df['col1'] / df['col2']

# 4. Aggregation
daily_sales = df.groupby('date')['amount'].sum()
```

#### C. Loading Patterns
- **Append**: Add new records (for transactional data)
- **Upsert**: Update existing or insert new (for dimensions)
- **Truncate & Load**: Replace entire table (for snapshots)

### When to Use Batch ETL
✅ Small to medium datasets (< 10GB)  
✅ Daily/hourly reporting requirements  
✅ Complex transformations requiring multiple passes  
✅ Source systems don't support streaming  

### Project Files
- `scripts/extract.py` - Data extraction logic
- `scripts/transform.py` - Business rules & cleaning
- `scripts/load.py` - Target loading
- `scripts/main.py` - Orchestration

---

## 2. Real-time Kafka Pipeline

### What is Stream Processing?
**Stream Processing** handles data in real-time as it arrives, enabling instant insights and actions.

### Architecture
```
[Producers] → [Kafka Broker] → [Consumers] → [Sink]
   (Apps)      (Topics/Partitions)  (Processing)  (DB/Alert)
```

### Key Concepts Learned

#### A. Kafka Fundamentals
- **Topic**: A category/feed name (e.g., "stock-ticks")
- **Partition**: Topics are split for parallelism
- **Producer**: Applications that publish messages
- **Consumer**: Applications that subscribe and process
- **Consumer Group**: Multiple consumers sharing load
- **Offset**: Position of consumer in the stream

#### B. Stream Processing Patterns
```python
# 1. Filtering
if tick.price > threshold:
    send_alert()

# 2. Aggregation (Windowing)
moving_avg = last_5_prices.mean()

# 3. Enrichment
tick_with_info = join(tick, reference_data)

# 4. Anomaly Detection
if deviation > 3_sigma:
    flag_as_anomaly()
```

#### C. Windowing Types
| Window Type | Description | Use Case |
|-------------|-------------|----------|
| **Tumbling** | Fixed-size, non-overlapping | Per-minute counts |
| **Sliding** | Fixed-size, overlapping | Last 5 minutes, updated every minute |
| **Session** | Gap-based | User activity sessions |

### When to Use Stream Processing
✅ Real-time dashboards  
✅ Fraud detection  
✅ IoT sensor monitoring  
✅ Alerting systems  
✅ Clickstream analysis  

### Project Files
- `src/producer.py` - Simulates stock ticks
- `src/consumer.py` - Processes streams, detects anomalies
- `config/settings.yaml` - Topic configurations

---

## 3. Spark Data Processing

### What is Apache Spark?
**Spark** is a distributed computing engine for large-scale data processing. It uses in-memory computation for speed.

### Architecture
```
[Driver Program]
     ↓
[Cluster Manager]
     ↓
[Executor Nodes] ← [Data Partitions]
```

### Key Concepts Learned

#### A. RDD vs DataFrame vs Dataset
| API Type | Optimization | Type Safety | Use Case |
|----------|--------------|-------------|----------|
| **RDD** | Low | Yes | Low-level control |
| **DataFrame** | Catalyst Optimizer | No (Python) | Most common |
| **Dataset** | Catalyst + Tungsten | Yes | Scala/Java typed |

#### B. Transformations (Lazy)
```python
# Narrow Transformations (same partition)
df.filter(df.amount > 100)
df.select("customer_id", "amount")
df.withColumn("profit", df.amount - df.cost)

# Wide Transformations (shuffle required)
df.groupBy("category").agg({"amount": "sum"})
df.join(other_df, "customer_id")
df.orderBy("date")
```

#### C. Actions (Trigger Execution)
```python
df.count()           # Count rows
df.show()            # Display sample
df.collect()         # Bring to driver
df.write.parquet()   # Save to disk
```

#### D. Advanced Analytics
```python
# Window Functions
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, sum

window_spec = Window.partitionBy("customer").orderBy("date")
df.withColumn("running_total", sum("amount").over(window_spec))

# RFM Analysis
rfm = df.groupBy("customer_id").agg(
    max("date").alias("recency"),
    count("*").alias("frequency"),
    sum("amount").alias("monetary")
)
```

### When to Use Spark
✅ Large datasets (GBs to PBs)  
✅ Complex transformations & joins  
✅ Machine Learning pipelines  
✅ Need for SQL-like queries on big data  

### Project Files
- `src/spark_session.py` - Spark configuration
- `src/transform.py` - Window functions, aggregations
- `src/main.py` - Full pipeline orchestration

---

## 4. Cloud Data Warehouse

### What is a Cloud Data Warehouse?
A **CDW** is a centralized repository for structured data optimized for analytics. Modern CDWs use **ELT** instead of ETL.

### Architecture (Medallion Design)
```
[Sources] → [Bronze/Raw] → [Silver/Cleaned] → [Gold/Dimensional] → [BI Tools]
            (S3/GCS)       (Validated)         (Aggregated)        (Tableau/PowerBI)
```

### Key Concepts Learned

#### A. ETL vs ELT
| Approach | Process | Best For |
|----------|---------|----------|
| **ETL** | Transform before loading | Legacy systems, sensitive data |
| **ELT** | Load raw first, transform in DW | Cloud DWs (Snowflake, BigQuery, Redshift) |

**Why ELT?**
- Leverages DW compute power
- Preserves raw data for reprocessing
- Faster initial load
- More flexible

#### B. Dimensional Modeling (Star Schema)
```
        [FactSales]
       /     |     \
      /      |      \
[DimCustomer] [DimProduct] [DimDate]
```

**Fact Tables:**
- Contains measurements/metrics
- Highly normalized
- Many rows (millions/billions)
- Example: `transaction_id, date_key, customer_key, amount`

**Dimension Tables:**
- Contains descriptive attributes
- Denormalized
- Fewer rows (thousands)
- Example: `customer_key, name, segment, region`

#### C. Slowly Changing Dimensions (SCD)

**Type 1 - Overwrite**
```
Before: Customer A, Region=NA
After:  Customer A, Region=EMEA  (old value lost)
```
Use when: History doesn't matter

**Type 2 - Add New Row**
```
Row 1: Customer A, Region=NA,  Valid: 2023-01-01 to 2023-06-30, Current=N
Row 2: Customer A, Region=EMEA, Valid: 2023-07-01 to NULL,    Current=Y
```
Use when: Historical tracking is required

**Type 3 - Add New Column**
```
Customer A, Current_Region=EMEA, Previous_Region=NA
```
Use when: Limited history needed

#### D. Data Quality Gates
```python
# 1. Completeness
assert df['customer_id'].isnull().sum() == 0

# 2. Uniqueness
assert df['transaction_id'].duplicated().sum() == 0

# 3. Referential Integrity
orphans = facts.merge(dim, how='left').filter(col('dim_key').isNull())
assert orphans.count() == 0

# 4. Validity
assert (df['amount'] > 0).all()
```

### When to Use Cloud DW
✅ Business Intelligence & Reporting  
✅ Historical analysis (years of data)  
✅ Multiple data sources integration  
✅ Self-service analytics for business users  

### Project Files
- `src/extractor.py` - Multi-source extraction
- `src/transformer.py` - SCD handling, dimensional modeling
- `src/loader.py` - Gold layer loading, auditing
- `src/dw_models.py` - Schema definitions

---

## Comparison & When to Use Each

### Decision Matrix

| Requirement | Best Choice | Why |
|-------------|-------------|-----|
| Daily sales report | **Batch ETL** | Simple, scheduled, cost-effective |
| Fraud detection | **Kafka Streaming** | Millisecond latency required |
| Customer segmentation (100M rows) | **Spark** | Distributed processing needed |
| Executive dashboard | **Cloud DW** | Star schema optimized for BI tools |
| IoT sensor data | **Kafka + Spark** | Stream ingestion + micro-batch processing |
| Historical trend analysis | **Cloud DW** | Dimensional modeling, time intelligence |
| ML feature engineering | **Spark** | Scalable transformations |
| Regulatory compliance (audit trail) | **Cloud DW (SCD2)** | Full history tracking |

### Modern Data Stack Integration
```
[Kafka] → [Spark Streaming] → [Cloud DW] → [BI Tools]
   ↑           ↑                  ↑
(Real-time)  (Micro-batch)    (Batch/ELT)
```

---

## Key Data Engineering Concepts

### 1. Data Modeling
- **Normalization**: Reduce redundancy (OLTP)
- **Denormalization**: Optimize reads (OLAP)
- **Star Schema**: One fact, many dimensions
- **Snowflake Schema**: Normalized dimensions

### 2. Partitioning & Clustering
```sql
-- Partition by date (physical separation)
PARTITION BY DATE(transaction_date)

-- Cluster by customer (sort within partitions)
CLUSTER BY customer_id
```
**Benefits**: Faster queries, cost reduction

### 3. Idempotency
Pipeline should produce same result if run multiple times:
```python
# NOT Idempotent
df.append(new_data)  # Duplicates on rerun

# Idempotent
df.drop_duplicates(subset=['id'])  # Safe to rerun
```

### 4. Backfilling
Historical data loading:
```python
for date in date_range(start, end):
    data = extract(date)
    load(data)
```

### 5. Monitoring & Observability
- **Data Freshness**: Is data up-to-date?
- **Volume Checks**: Did row counts change unexpectedly?
- **Schema Validation**: Did columns change?
- **Quality Metrics**: Null rates, duplicate rates

### 6. Cost Optimization
| Strategy | Impact |
|----------|--------|
| Partition pruning | Reduce scan volume |
| Columnar storage (Parquet) | Better compression |
| Compression (Snappy, GZIP) | Lower storage costs |
| Lifecycle policies | Archive old data |

---

## Learning Path Recommendation

1. **Start with Batch ETL** - Understand fundamentals
2. **Move to Cloud DW** - Learn dimensional modeling
3. **Learn Spark** - Handle big data
4. **Add Kafka** - Real-time capabilities

### Next Steps
- Explore orchestration tools (Airflow, Dagster)
- Learn cloud platforms (AWS, GCP, Azure)
- Study data governance & security
- Practice with real datasets

---

## Glossary

| Term | Definition |
|------|------------|
| **Batch** | Processing data in groups at scheduled intervals |
| **Stream** | Processing data continuously as it arrives |
| **Latency** | Time between data generation and availability |
| **Throughput** | Volume of data processed per unit time |
| **Idempotent** | Operation that can be applied multiple times without changing result |
| **Surrogate Key** | System-generated unique identifier (vs natural key) |
| **Grain** | Level of detail in a fact table |
| **Slowly Changing Dimension** | Technique to track attribute changes over time |

---

*This guide covers the fundamental concepts demonstrated in the four projects. Each project can be extended with additional features based on specific business requirements.*
