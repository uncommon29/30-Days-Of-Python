"""Extractor: Simulates pulling data from Cloud Sources (S3, API, Stream)."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

class DataExtractor:
    """Simulates extraction from various cloud sources."""
    
    def __init__(self):
        self.base_date = datetime.now()
        
    def extract_customers(self, n_records=500):
        """Simulate extracting customer data from an API."""
        print(f"Extracting {n_records} customers from simulated API...")
        
        segments = ['Enterprise', 'SMB', 'Consumer', 'Startup']
        regions = ['NA', 'EMEA', 'APAC', 'LATAM']
        
        data = {
            'customer_id': [f"CUST_{i:05d}" for i in range(1, n_records + 1)],
            'name': [f"Customer {i}" for i in range(1, n_records + 1)],
            'email': [f"customer{i}@example.com" for i in range(1, n_records + 1)],
            'segment': np.random.choice(segments, n_records),
            'region': np.random.choice(regions, n_records),
            'created_at': [(self.base_date - timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d') 
                          for _ in range(n_records)]
        }
        
        # Simulate some updates for SCD Type 2 demonstration
        df = pd.DataFrame(data)
        return df
        
    def extract_products(self, n_records=100):
        """Simulate extracting product catalog from a file."""
        print(f"Extracting {n_records} products from simulated file...")
        
        categories = ['Electronics', 'Clothing', 'Home', 'Books', 'Sports']
        subcategories = {
            'Electronics': ['Phones', 'Laptops', 'Accessories'],
            'Clothing': ['Men', 'Women', 'Kids'],
            'Home': ['Furniture', 'Decor', 'Kitchen'],
            'Books': ['Fiction', 'Non-Fiction', 'Technical'],
            'Sports': ['Equipment', 'Apparel', 'Outdoor']
        }
        
        data = []
        for i in range(1, n_records + 1):
            cat = np.random.choice(categories)
            subcat = np.random.choice(subcategories[cat])
            price = round(np.random.uniform(10, 1000), 2)
            data.append({
                'product_id': f"PROD_{i:04d}",
                'name': f"Product {i} ({subcat})",
                'category': cat,
                'subcategory': subcat,
                'price': price,
                'cost': round(price * 0.6, 2)
            })
            
        return pd.DataFrame(data)
        
    def extract_sales(self, n_records=5000):
        """Simulate extracting sales transactions from a stream."""
        print(f"Extracting {n_records} sales transactions from simulated stream...")
        
        customer_ids = [f"CUST_{i:05d}" for i in range(1, 501)]
        product_ids = [f"PROD_{i:04d}" for i in range(1, 101)]
        
        data = {
            'transaction_id': [f"TXN_{i:08d}" for i in range(1, n_records + 1)],
            'customer_id': np.random.choice(customer_ids, n_records),
            'product_id': np.random.choice(product_ids, n_records),
            'transaction_date': [(self.base_date - timedelta(
                days=np.random.randint(0, 90), 
                hours=np.random.randint(0, 24)
            )).strftime('%Y-%m-%d %H:%M:%S') for _ in range(n_records)],
            'quantity': np.random.randint(1, 10, n_records),
            'unit_price': np.random.uniform(10, 500, n_records),
            'discount': np.round(np.random.uniform(0, 0.2, n_records), 2)
        }
        
        df = pd.DataFrame(data)
        df['amount'] = df['quantity'] * df['unit_price'] * (1 - df['discount'])
        return df

    def save_bronze(self, df, name, output_dir="../data/bronze"):
        """Save raw data to Bronze layer."""
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, f"{name}_raw.csv")
        df.to_csv(path, index=False)
        print(f"Saved {len(df)} records to Bronze layer: {path}")
        return path

if __name__ == "__main__":
    ext = DataExtractor()
    c_df = ext.extract_customers(100)
    p_df = ext.extract_products(50)
    s_df = ext.extract_sales(500)
    print("Extraction complete.")
