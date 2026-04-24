"""
Data Manager - Local Dataset Integration
Handles loading and managing marketing datasets from local CSV files
"""

import os
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple
import pickle
from datetime import datetime


class DataManager:
    """Manages marketing datasets from local CSV files"""
    
    def __init__(self, data_dir: str = r"E:\destiny\data"):
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            print(f"[DATA] Creating directory: {data_dir}")
            os.makedirs(data_dir, exist_ok=True)
        
        # Map dataset names to your file names
        self.local_datasets = {
            'campaign_performance': 'ad_campaign_data.csv',
            'ad_engagement': 'Social_Media_Advertising.csv',
            'engagement_metrics': 'Social Media Engagement Dataset.csv',
            'viral_trends': 'Cleaned_Viral_Social_Media_Trends.csv',
            'marketing_campaign': 'marketing_campaign_dataset.csv',
            'viral_original': 'Viral_Social_Media_Trends.csv'
        }
        
        self.loaded_datasets = {}
        self.dataset_stats = {}
    
    def load_dataset(self, dataset_name: str, use_synthetic_fallback: bool = True) -> pd.DataFrame:
        """Load dataset from local files"""
        if dataset_name in self.loaded_datasets:
            return self.loaded_datasets[dataset_name]
        
        if dataset_name in self.local_datasets:
            file_name = self.local_datasets[dataset_name]
            file_path = os.path.join(self.data_dir, file_name)
            
            if os.path.exists(file_path):
                try:
                    df = pd.read_csv(file_path)
                    print(f"[DATA] Loaded {file_name}: {df.shape[0]} rows, {df.shape[1]} columns")
                    df = self._preprocess_dataset(df, dataset_name)
                    self.loaded_datasets[dataset_name] = df
                    return df
                except Exception as e:
                    print(f"[DATA] Error loading {file_name}: {e}")
        
        if use_synthetic_fallback:
            print(f"[DATA] Generating synthetic data for {dataset_name}")
            return self._generate_synthetic_data(dataset_name)
        
        return pd.DataFrame()
    
    def _preprocess_dataset(self, df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
        """Clean and preprocess dataset"""
        if df.empty:
            return df
        
        df_processed = df.copy()
        
        # Standardize column names
        df_processed.columns = [str(col).strip().lower().replace(' ', '_').replace('-', '_') 
                               for col in df_processed.columns]
        
        # Remove duplicates
        df_processed = df_processed.drop_duplicates()
        
        # Handle missing values
        numeric_cols = df_processed.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df_processed[col].isnull().sum() > 0:
                median_val = df_processed[col].median()
                df_processed[col] = df_processed[col].fillna(median_val)
        
        categorical_cols = df_processed.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if df_processed[col].isnull().sum() > 0:
                mode_val = df_processed[col].mode()[0] if not df_processed[col].mode().empty else 'Unknown'
                df_processed[col] = df_processed[col].fillna(mode_val)
        
        # Create marketing metrics if they don't exist
        if 'impressions' in df_processed.columns and 'clicks' in df_processed.columns:
            df_processed['ctr'] = (df_processed['clicks'] / df_processed['impressions'] * 100).round(3)
        
        if 'clicks' in df_processed.columns and 'conversions' in df_processed.columns:
            df_processed['conversion_rate'] = (df_processed['conversions'] / df_processed['clicks'] * 100).round(3)
        
        if 'likes' in df_processed.columns and 'impressions' in df_processed.columns:
            df_processed['engagement_rate'] = (df_processed['likes'] / df_processed['impressions'] * 100).round(3)
        
        if 'revenue' in df_processed.columns and 'budget' in df_processed.columns:
            df_processed['roi'] = ((df_processed['revenue'] - df_processed['budget']) / df_processed['budget'] * 100).round(2)
        
        return df_processed
    
    def _generate_synthetic_data(self, dataset_name: str) -> pd.DataFrame:
        """Generate synthetic data if files not found"""
        np.random.seed(42)
        n_samples = 5000
        
        print(f"[DATA] Generating {n_samples} synthetic samples for {dataset_name}")
        
        if 'campaign' in dataset_name.lower():
            data = {
                'campaign_id': [f'camp_{i:04d}' for i in range(n_samples)],
                'campaign_name': [f'Campaign_{np.random.choice(["Q1", "Q2", "Q3", "Q4"])}_{i}' 
                                 for i in range(n_samples)],
                'platform': np.random.choice(['Facebook', 'Instagram', 'LinkedIn', 'Twitter', 'TikTok'], n_samples),
                'budget': np.random.uniform(1000, 50000, n_samples),
                'duration_days': np.random.randint(7, 90, n_samples),
                'impressions': np.random.randint(10000, 1000000, n_samples),
                'clicks': np.random.randint(500, 50000, n_samples),
                'conversions': np.random.randint(50, 5000, n_samples),
                'revenue': np.random.uniform(2000, 100000, n_samples)
            }
        elif 'engagement' in dataset_name.lower():
            data = {
                'post_id': [f'post_{i:06d}' for i in range(n_samples)],
                'platform': np.random.choice(['Instagram', 'TikTok', 'Facebook', 'Twitter', 'LinkedIn'], n_samples),
                'content_type': np.random.choice(['Image', 'Video', 'Reel', 'Story', 'Text'], n_samples),
                'hashtag_count': np.random.randint(0, 25, n_samples),
                'impressions': np.random.randint(1000, 100000, n_samples),
                'likes': np.random.randint(50, 50000, n_samples),
                'comments': np.random.randint(0, 5000, n_samples),
                'shares': np.random.randint(0, 10000, n_samples)
            }
        else:
            data = {
                'id': [f'item_{i}' for i in range(n_samples)],
                'metric_value': np.random.uniform(0, 100, n_samples),
                'category': np.random.choice(['A', 'B', 'C', 'D', 'E'], n_samples),
                'platform': np.random.choice(['Facebook', 'Instagram', 'LinkedIn'], n_samples)
            }
        
        df = pd.DataFrame(data)
        
        # Add calculated metrics
        if 'impressions' in df.columns and 'clicks' in df.columns:
            df['ctr'] = (df['clicks'] / df['impressions'] * 100).round(3)
        
        if 'clicks' in df.columns and 'conversions' in df.columns:
            df['conversion_rate'] = (df['conversions'] / df['clicks'] * 100).round(3)
        
        if 'likes' in df.columns and 'impressions' in df.columns:
            df['engagement_rate'] = (df['likes'] / df['impressions'] * 100).round(3)
        
        if 'revenue' in df.columns and 'budget' in df.columns:
            df['roi'] = ((df['revenue'] - df['budget']) / df['budget'] * 100).round(2)
        
        self.loaded_datasets[dataset_name] = df
        return df
    
    def load_all_datasets(self) -> Dict[str, pd.DataFrame]:
        """Load all available datasets"""
        all_datasets = {}
        
        print(f"[DATA] Loading datasets from {self.data_dir}")
        
        # Check directory exists
        if not os.path.exists(self.data_dir):
            print(f"[DATA] Directory not found: {self.data_dir}")
            return all_datasets
        
        # Try to load all CSV files
        try:
            csv_files = [f for f in os.listdir(self.data_dir) if f.endswith('.csv')]
            print(f"[DATA] Found {len(csv_files)} CSV files")
            
            if not csv_files:
                print("[DATA] No CSV files found, generating synthetic data")
                for dataset_name in ['campaign_performance', 'ad_engagement', 'engagement_metrics']:
                    all_datasets[dataset_name] = self._generate_synthetic_data(dataset_name)
                return all_datasets
            
            for csv_file in csv_files:
                try:
                    file_path = os.path.join(self.data_dir, csv_file)
                    print(f"[DATA] Reading {csv_file}...")
                    df = pd.read_csv(file_path)
                    
                    # Determine dataset name
                    dataset_name = csv_file.replace('.csv', '').replace(' ', '_').lower()
                    
                    # Check if it's a known dataset
                    for known_name, known_file in self.local_datasets.items():
                        if known_file.lower() == csv_file.lower():
                            dataset_name = known_name
                            break
                    
                    # Preprocess
                    df = self._preprocess_dataset(df, dataset_name)
                    all_datasets[dataset_name] = df
                    print(f"[DATA] ✓ Loaded {csv_file}: {df.shape[0]} rows")
                    
                except Exception as e:
                    print(f"[DATA] ⚠ Failed to load {csv_file}: {e}")
                    continue
        
        except Exception as e:
            print(f"[DATA] Error accessing directory: {e}")
            # Generate synthetic data as fallback
            for dataset_name in ['campaign_performance', 'ad_engagement', 'engagement_metrics']:
                all_datasets[dataset_name] = self._generate_synthetic_data(dataset_name)
        
        return all_datasets
    
    def get_dataset_statistics(self) -> Dict[str, Any]:
        """Get statistics about loaded datasets"""
        stats = {
            'available_datasets': len(self.local_datasets),
            'loaded_datasets': len(self.loaded_datasets),
            'dataset_details': {},
            'local_files': [],
            'local_file_count': 0
        }
        
        # Get details of loaded datasets
        for name, df in self.loaded_datasets.items():
            stats['dataset_details'][name] = {
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': list(df.columns)[:10],  # First 10 columns
                'memory_mb': round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2)
            }
        
        # Get file info from directory
        try:
            if os.path.exists(self.data_dir):
                csv_files = [f for f in os.listdir(self.data_dir) if f.endswith('.csv')]
                stats['local_files'] = csv_files
                stats['local_file_count'] = len(csv_files)
                stats['available_datasets'] = len(csv_files)  # Update with actual count
        except Exception as e:
            print(f"[DATA] Error reading directory: {e}")
        
        return stats
    
    def save_trained_model(self, model: Any, model_name: str):
        """Save trained model to disk"""
        model_dir = os.path.join(self.data_dir, 'models')
        os.makedirs(model_dir, exist_ok=True)
        
        model_path = os.path.join(model_dir, f"{model_name}.pkl")
        
        try:
            with open(model_path, 'wb') as f:
                pickle.dump(model, f)
            print(f"[DATA] Saved model: {model_name} to {model_path}")
        except Exception as e:
            print(f"[DATA] Error saving model {model_name}: {e}")
    
    def load_trained_model(self, model_name: str) -> Any:
        """Load trained model from disk"""
        model_dir = os.path.join(self.data_dir, 'models')
        model_path = os.path.join(model_dir, f"{model_name}.pkl")
        
        if not os.path.exists(model_path):
            print(f"[DATA] Model file not found: {model_path}")
            return None
        
        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            print(f"[DATA] Loaded model: {model_name}")
            return model
        except Exception as e:
            print(f"[DATA] Error loading model {model_name}: {e}")
            return None