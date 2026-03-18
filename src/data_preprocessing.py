"""
Data Preprocessing Module

This module handles all data loading, cleaning, encoding, and splitting operations.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_data(filepath):
    """
    Load dataset from CSV file.
    
    Args:
        filepath (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: Loaded dataset
    """
    try:
        data = pd.read_csv(filepath)
        logger.info(f"Dataset loaded successfully. Shape: {data.shape}")
        return data
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        raise
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise


def drop_identifier_columns(data, columns=['LoanID']):
    """
    Drop identifier columns that are not useful for modeling.
    
    Args:
        data (pd.DataFrame): Input dataset
        columns (list): List of columns to drop
        
    Returns:
        pd.DataFrame: Dataset with identifier columns removed
    """
    data_cleaned = data.drop(columns=columns, errors='ignore')
    logger.info(f"Dropped columns: {columns}")
    return data_cleaned


def encode_categorical_features(data, categorical_cols=None):
    """
    Encode categorical features using LabelEncoder.
    
    Args:
        data (pd.DataFrame): Input dataset
        categorical_cols (list, optional): List of categorical columns. 
                                          If None, auto-detect object dtypes
        
    Returns:
        tuple: (encoded_data, encoders_dict)
    """
    data_encoded = data.copy()
    encoders = {}
    
    # Auto-detect categorical columns if not provided
    if categorical_cols is None:
        categorical_cols = data_encoded.select_dtypes(include=['object']).columns
    
    for col in categorical_cols:
        if col in data_encoded.columns:
            le = LabelEncoder()
            data_encoded[col] = le.fit_transform(data_encoded[col].astype(str))
            encoders[col] = le
            logger.info(f"Encoded column: {col}")
    
    return data_encoded, encoders


def split_features_target(data, target_col='Default'):
    """
    Separate features and target variable.
    
    Args:
        data (pd.DataFrame): Input dataset
        target_col (str): Name of target column
        
    Returns:
        tuple: (X, y)
    """
    if target_col not in data.columns:
        logger.error(f"Target column '{target_col}' not found in dataset")
        raise ValueError(f"Target column '{target_col}' not found")
    
    X = data.drop(target_col, axis=1)
    y = data[target_col]
    
    logger.info(f"Features shape: {X.shape}, Target shape: {y.shape}")
    return X, y


def train_test_split_data(X, y, test_size=0.2, random_state=42):
    """
    Split data into training and testing sets.
    
    Args:
        X (pd.DataFrame): Features
        y (pd.Series): Target variable
        test_size (float): Proportion of test set
        random_state (int): Random seed for reproducibility
        
    Returns:
        tuple: (X_train, X_test, y_train, y_test)
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    logger.info(f"Training set size: {X_train.shape[0]}")
    logger.info(f"Testing set size: {X_test.shape[0]}")
    logger.info(f"Train-test split ratio: {(1-test_size):.0%}-{test_size:.0%}")
    
    return X_train, X_test, y_train, y_test


def preprocess_pipeline(data_path, target_col='Default', test_size=0.2, random_state=42):
    """
    Complete preprocessing pipeline.
    
    Args:
        data_path (str): Path to raw data CSV
        target_col (str): Name of target column
        test_size (float): Proportion of test set
        random_state (int): Random seed
        
    Returns:
        dict: Dictionary containing X_train, X_test, y_train, y_test, encoders
    """
    logger.info("Starting preprocessing pipeline...")
    
    # Load data
    data = load_data(data_path)
    
    # Drop identifier columns
    data = drop_identifier_columns(data)
    
    # Encode categorical features
    data, encoders = encode_categorical_features(data)
    
    # Split features and target
    X, y = split_features_target(data, target_col)
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split_data(X, y, test_size, random_state)
    
    logger.info("Preprocessing pipeline completed successfully!")
    
    return {
        'X_train': X_train,
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test,
        'encoders': encoders,
        'feature_names': X.columns.tolist()
    }


if __name__ == "__main__":
    from pathlib import Path
    
    # Get project root directory
    project_root = Path(__file__).parent.parent
    data_path = project_root / "data" / "raw" / "Loan_default.csv"
    
    # Example usage
    result = preprocess_pipeline(str(data_path))
    print("\nPreprocessing Complete!")
    print(f"Training features shape: {result['X_train'].shape}")
    print(f"Testing features shape: {result['X_test'].shape}")
