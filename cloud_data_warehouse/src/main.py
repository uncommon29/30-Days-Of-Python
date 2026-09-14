"""Main Orchestration Script for Cloud Data Warehouse Pipeline."""

import os
import sys
from datetime import datetime
import uuid

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from extractor import DataExtractor
from transformer import DataTransformer
from loader import DataLoader

def run_pipeline():
    """Execute the full ELT pipeline."""
    print("="*60)
    print("CLOUD DATA WAREHOUSE PIPELINE - START")
    print("="*60)
    
    start_time = datetime.now()
    run_id = str(uuid.uuid4())[:8]
    
    # Initialize components
    extractor = DataExtractor()
    transformer = DataTransformer()
    loader = DataLoader(output_dir="../output")
    
    try:
        # ===========================
        # 1. EXTRACT (Bronze Layer)
        # ===========================
        print("\n[PHASE 1] EXTRACTION")
        
        raw_customers = extractor.extract_customers(n_records=500)
        extractor.save_bronze(raw_customers, "customers", output_dir="../data/bronze")
        
        raw_products = extractor.extract_products(n_records=100)
        extractor.save_bronze(raw_products, "products", output_dir="../data/bronze")
        
        raw_sales = extractor.extract_sales(n_records=5000)
        extractor.save_bronze(raw_sales, "sales", output_dir="../data/bronze")
        
        # ===========================
        # 2. TRANSFORM (Silver/Gold)
        # ===========================
        print("\n[PHASE 2] TRANSFORMATION")
        
        # Clean data (Silver)
        clean_customers = transformer.clean_customers(raw_customers)
        clean_products = transformer.clean_products(raw_products)
        clean_sales = transformer.clean_sales(raw_sales)
        
        # Create Dimensions (Gold)
        dim_customer_path = "../output/dim_customer.csv"
        dim_customer = transformer.create_customer_dimension(
            clean_customers, 
            existing_dim=dim_customer_path if os.path.exists(dim_customer_path) else None
        )
        
        dim_product = transformer.create_product_dimension(clean_products)
        
        # Create Fact Table (Gold)
        fact_sales = transformer.create_sales_fact(clean_sales, dim_customer, dim_product)
        
        # ===========================
        # 3. LOAD (Gold Layer)
        # ===========================
        print("\n[PHASE 3] LOADING")
        
        cust_count = loader.load_dimension(dim_customer, "dim_customer")
        prod_count = loader.load_dimension(dim_product, "dim_product")
        sales_count = loader.load_fact(fact_sales, "fact_sales")
        
        # Audit Logging
        loader.log_audit(run_id, "dim_customer", len(raw_customers), cust_count, "SUCCESS", start_time)
        loader.log_audit(run_id, "dim_product", len(raw_products), prod_count, "SUCCESS", start_time)
        loader.log_audit(run_id, "fact_sales", len(raw_sales), sales_count, "SUCCESS", start_time)
        
        # ===========================
        # SUMMARY
        # ===========================
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print("\n" + "="*60)
        print("PIPELINE EXECUTION SUMMARY")
        print("="*60)
        print(f"Run ID: {run_id}")
        print(f"Status: SUCCESS")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Customers Loaded: {cust_count}")
        print(f"Products Loaded: {prod_count}")
        print(f"Sales Transactions Loaded: {sales_count}")
        print(f"Output Directory: ../output/")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\nERROR: Pipeline failed with exception: {str(e)}")
        loader.log_audit(run_id, "pipeline", 0, 0, "FAILED", start_time, error=str(e))
        return False

if __name__ == "__main__":
    success = run_pipeline()
    sys.exit(0 if success else 1)
