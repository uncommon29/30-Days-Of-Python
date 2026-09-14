"""Transformer: Business Logic, Cleaning, and SCD Handling."""

import pandas as pd
import numpy as np
from datetime import datetime
import os

class DataTransformer:
    """Handles transformation logic for ELT pipeline."""
    
    def __init__(self):
        self.surrogate_key_counter = {}
        
    def clean_customers(self, df):
        """Clean and standardize customer data (Silver Layer)."""
        print("Cleaning customer data...")
        df = df.copy()
        
        # Standardize email
        df['email'] = df['email'].str.lower().str.strip()
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['customer_id'])
        
        # Handle nulls
        df['segment'] = df['segment'].fillna('Unknown')
        df['region'] = df['region'].fillna('Unknown')
        
        return df
        
    def clean_products(self, df):
        """Clean product catalog."""
        print("Cleaning product data...")
        df = df.copy()
        
        # Ensure positive prices
        df = df[df['price'] > 0]
        df = df[df['cost'] > 0]
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['product_id'])
        
        return df
        
    def clean_sales(self, df):
        """Clean sales transactions."""
        print("Cleaning sales data...")
        df = df.copy()
        
        # Filter invalid transactions
        df = df[df['quantity'] > 0]
        df = df[df['amount'] > 0]
        
        # Convert date
        df['transaction_date'] = pd.to_datetime(df['transaction_date'])
        df['date_key'] = df['transaction_date'].dt.strftime('%Y%m%d').astype(int)
        
        return df
        
    def create_customer_dimension(self, df, existing_dim=None):
        """
        Create Customer Dimension with SCD Type 2 logic.
        Tracks historical changes in customer attributes.
        """
        print("Creating Customer Dimension (SCD Type 2)...")
        
        df = df.copy()
        now = datetime.now()
        
        if existing_dim is None or not os.path.exists(existing_dim):
            # Initial load
            df['customer_key'] = range(1, len(df) + 1)
            df['is_current'] = True
            df['valid_from'] = now
            df['valid_to'] = pd.NaT
            
            return df[['customer_id', 'customer_key', 'name', 'email', 'segment', 
                       'region', 'is_current', 'valid_from', 'valid_to']]
        else:
            # Incremental load with SCD Type 2
            existing = pd.read_csv(existing_dim)
            existing['valid_from'] = pd.to_datetime(existing['valid_from'])
            existing['valid_to'] = pd.to_datetime(existing['valid_to'], errors='coerce')
            
            new_keys = []
            updates = []
            
            # Simple simulation: assign new keys for new customers
            max_key = existing['customer_key'].max() if not existing.empty else 0
            
            result_rows = []
            for _, row in df.iterrows():
                cust_id = row['customer_id']
                
                # Check if customer exists
                existing_cust = existing[existing['customer_id'] == cust_id]
                
                if existing_cust.empty:
                    # New customer
                    max_key += 1
                    row['customer_key'] = max_key
                    row['is_current'] = True
                    row['valid_from'] = now
                    row['valid_to'] = pd.NaT
                    result_rows.append(row)
                else:
                    # Existing customer - check for changes (simulated as no change for simplicity)
                    # In real scenario, compare attributes and expire old record if changed
                    curr = existing_cust[existing_cust['is_current'] == True]
                    if not curr.empty:
                        row['customer_key'] = curr.iloc[0]['customer_key']
                        row['is_current'] = True
                        row['valid_from'] = curr.iloc[0]['valid_from']
                        row['valid_to'] = pd.NaT
                        result_rows.append(row)
            
            result_df = pd.DataFrame(result_rows)
            return result_df[['customer_id', 'customer_key', 'name', 'email', 'segment', 
                              'region', 'is_current', 'valid_from', 'valid_to']]
                              
    def create_product_dimension(self, df):
        """Create Product Dimension (SCD Type 1 - overwrite)."""
        print("Creating Product Dimension (SCD Type 1)...")
        
        df = df.copy()
        df['product_key'] = range(1, len(df) + 1)
        
        return df[['product_id', 'product_key', 'name', 'category', 'subcategory', 'price', 'cost']]
        
    def create_sales_fact(self, sales_df, cust_dim, prod_dim):
        """Join sales with dimensions to create Fact table."""
        print("Creating Sales Fact Table...")
        
        # Merge with dimensions
        fact = sales_df.merge(cust_dim[['customer_id', 'customer_key']], on='customer_id', how='left')
        fact = fact.merge(prod_dim[['product_id', 'product_key']], on='product_id', how='left')
        
        # Calculate profit
        fact = fact.merge(prod_dim[['product_key', 'cost']], on='product_key', how='left')
        fact['profit'] = fact['amount'] - (fact['quantity'] * fact['cost'])
        
        # Handle nulls (referential integrity issues)
        null_cust = fact['customer_key'].isnull().sum()
        null_prod = fact['product_key'].isnull().sum()
        
        if null_cust > 0 or null_prod > 0:
            print(f"Warning: {null_cust} orphan customers, {null_prod} orphan products found.")
            fact = fact.dropna(subset=['customer_key', 'product_key'])
        
        # Select final columns
        fact = fact[['transaction_id', 'date_key', 'customer_key', 'product_key', 
                     'amount', 'quantity', 'discount', 'profit']]
                     
        return fact

if __name__ == "__main__":
    print("Transformer module loaded.")
