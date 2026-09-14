"""Loader: Loads data into Warehouse (Gold Layer) and handles auditing."""

import pandas as pd
import os
from datetime import datetime
import uuid

class DataLoader:
    """Handles loading data to the Data Warehouse."""
    
    def __init__(self, output_dir="../output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def load_dimension(self, df, table_name):
        """Load a dimension table."""
        path = os.path.join(self.output_dir, f"{table_name}.csv")
        
        # Check if file exists to append or overwrite
        if os.path.exists(path):
            existing = pd.read_csv(path)
            # For SCD Type 1, we might overwrite; for Type 2, we append
            if table_name == 'dim_customer':
                # Append new records (SCD Type 2 simulation)
                df = pd.concat([existing, df], ignore_index=True).drop_duplicates(subset=['customer_key'])
            else:
                # Overwrite for Product (SCD Type 1)
                pass
        
        df.to_csv(path, index=False)
        print(f"Loaded {len(df)} rows to {table_name} at {path}")
        return len(df)
        
    def load_fact(self, df, table_name):
        """Load a fact table."""
        path = os.path.join(self.output_dir, f"{table_name}.csv")
        
        # Facts are typically appended
        if os.path.exists(path):
            existing = pd.read_csv(path)
            df = pd.concat([existing, df], ignore_index=True)
            # Remove duplicate transactions
            df = df.drop_duplicates(subset=['transaction_id'])
            
        df.to_csv(path, index=False)
        print(f"Loaded {len(df)} rows to {table_name} at {path}")
        return len(df)
        
    def log_audit(self, run_id, table_name, rows_processed, rows_loaded, status, start_time, error=None):
        """Log audit information."""
        audit_path = os.path.join(self.output_dir, "audit_log.csv")
        
        record = {
            'run_id': run_id,
            'table_name': table_name,
            'rows_processed': rows_processed,
            'rows_loaded': rows_loaded,
            'status': status,
            'start_time': start_time,
            'end_time': datetime.now(),
            'error_message': error if error else ''
        }
        
        audit_df = pd.DataFrame([record])
        
        if os.path.exists(audit_path):
            existing = pd.read_csv(audit_path)
            audit_df = pd.concat([existing, audit_df], ignore_index=True)
            
        audit_df.to_csv(audit_path, index=False)
        print(f"Audit log updated for {table_name}: {status}")

if __name__ == "__main__":
    print("Loader module loaded.")
