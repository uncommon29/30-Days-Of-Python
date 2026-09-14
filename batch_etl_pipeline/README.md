# Batch ETL Pipeline Project

## Overview
This project implements a batch ETL (Extract, Transform, Load) pipeline using Python. It processes public dataset data through extraction, transformation, and loading stages with proper logging, error handling, and configuration management.

## Dataset
We use the **Iris Dataset** - a classic public dataset containing measurements of iris flowers from three different species. This dataset is perfect for demonstrating ETL processes as it contains:
- Numeric features (sepal length, sepal width, petal length, petal width)
- Categorical data (species names)
- Clean structure suitable for transformation operations

## Project Structure
```
batch_etl_pipeline/
├── config/
│   └── config.yaml          # Configuration file
├── data/
│   ├── raw/                 # Raw extracted data
│   ├── processed/           # Transformed data
│   └── output/              # Final loaded data
├── scripts/
│   ├── extract.py           # Extraction module
│   ├── transform.py         # Transformation module
│   ├── load.py              # Loading module
│   └── main.py              # Main pipeline orchestrator
├── logs/                    # Log files
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Features
- **Modular Design**: Separate modules for Extract, Transform, and Load operations
- **Configuration Management**: YAML-based configuration for easy parameter updates
- **Logging**: Comprehensive logging for monitoring and debugging
- **Error Handling**: Robust error handling with graceful failures
- **Data Validation**: Input validation at each stage
- **Reproducibility**: Consistent results with seed values and version control

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd batch_etl_pipeline
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the complete ETL pipeline:
```bash
python scripts/main.py
```

Or run individual stages:
```bash
# Extract only
python scripts/extract.py

# Transform only (requires extracted data)
python scripts/transform.py

# Load only (requires transformed data)
python scripts/load.py
```

## Pipeline Stages

### 1. Extract
- Downloads/fetches the Iris dataset
- Saves raw data to `data/raw/` directory
- Validates data presence and basic structure

### 2. Transform
- Loads raw data
- Performs data cleaning (handles missing values if any)
- Adds derived features (e.g., petal ratio, sepal area)
- Normalizes numeric columns
- Encodes categorical variables
- Saves processed data to `data/processed/` directory

### 3. Load
- Loads processed data
- Aggregates data by species
- Creates summary statistics
- Exports final datasets to `data/output/` directory in multiple formats (CSV, JSON)

## Configuration

Edit `config/config.yaml` to customize:
- Data paths
- Processing parameters
- Logging levels
- Output formats

## Output Files

After running the pipeline, you'll find:
- `data/raw/iris_raw.csv` - Original extracted data
- `data/processed/iris_processed.csv` - Cleaned and transformed data
- `data/output/iris_final.csv` - Final dataset ready for analysis
- `data/output/iris_summary.json` - Summary statistics by species
- `logs/etl_pipeline.log` - Detailed execution logs

## Requirements
- Python 3.8+
- pandas
- numpy
- pyyaml
- scikit-learn (optional, for advanced transformations)

## License
MIT License

## Author
Created as a demonstration of batch ETL pipeline best practices.
