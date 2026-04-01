import pandas as pd
import logging

logger = logging.getLogger(__name__)

CATEGORICAL_MAPPINGS = {
    'Education': {'High School': 1, 'HS': 1, "Bachelor's": 2, 'Bachelor': 2, "Master's": 3, 'Master': 3},
    'EmploymentType': {'Self-Employed': 0, 'Self-employed': 0, 'Salaried': 1},
    'MaritalStatus': {'Single': 0, 'Married': 1},
    'LoanPurpose': {'Auto': 0, 'Home': 1, 'Personal': 2},
}

REQUIRED_FEATURES = [
    'Age', 'Income', 'LoanAmount', 'CreditScore', 'MonthsEmployed',
    'NumCreditLines', 'InterestRate', 'LoanTerm', 'DTIRatio',
    'Education', 'EmploymentType', 'MaritalStatus', 'HasMortgage',
    'HasDependents', 'LoanPurpose', 'HasCoSigner'
]


def encode_batch_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Encode categorical variables, handle missing values, and ensure correct feature structure.
    
    Args:
        df: Input dataframe with mixed data types
        
    Returns:
        Encoded dataframe with all numeric values in correct order
    """
    df_encoded = df.copy()
    
    logger.info(f"Starting batch encoding: input shape {df_encoded.shape}, columns: {df_encoded.columns.tolist()}")
    
    # Encode categorical columns
    for col, mapping in CATEGORICAL_MAPPINGS.items():
        if col in df_encoded.columns:
            if df_encoded[col].dtype == 'object':
                df_encoded[col] = df_encoded[col].map(mapping)
                df_encoded[col] = pd.to_numeric(df_encoded[col], errors='coerce')
                logger.info(f"Encoded categorical column: {col}")
    
    # Convert remaining object columns to numeric
    for col in df_encoded.select_dtypes(include=['object']).columns:
        if col not in ['LoanID', 'Default', 'id', 'CustomerID', 'target', 'loan_status']:
            try:
                df_encoded[col] = pd.to_numeric(df_encoded[col], errors='coerce')
                logger.info(f"Converted {col} to numeric")
            except Exception as e:
                logger.warning(f"Could not convert {col}: {str(e)}")
    
    # Handle missing values
    missing_count = df_encoded.isnull().sum().sum()
    if missing_count > 0:
        logger.warning(f"Found {missing_count} missing values, filling with mean")
        numeric_cols = df_encoded.select_dtypes(include=['number']).columns
        df_encoded[numeric_cols] = df_encoded[numeric_cols].fillna(df_encoded[numeric_cols].mean())

    # Drop explicit non-feature columns that may appear in raw or cleaned datasets
    non_feature_cols = ['LoanID', 'Default', 'target', 'loan_status', 'id', 'CustomerID', 'Loan_ID', 'Status']
    for col in non_feature_cols:
        if col in df_encoded.columns:
            df_encoded.drop(columns=[col], inplace=True)
            logger.info(f"Dropped non-feature column: {col}")

    # Warn for extra non-model columns and drop them
    extra_cols = [c for c in df_encoded.columns if c not in REQUIRED_FEATURES]
    if extra_cols:
        logger.warning(f"Dropping unexpected columns: {extra_cols}")
        df_encoded = df_encoded.drop(columns=extra_cols, errors='ignore')

    # Enforce required feature order and fill any missing feature columns with zeros
    missing_features = [col for col in REQUIRED_FEATURES if col not in df_encoded.columns]
    if missing_features:
        logger.warning(f"Missing expected columns will be added with default 0 values: {missing_features}")
        for col in missing_features:
            df_encoded[col] = 0.0

    # Reindex to enforce exact column order
    df_encoded = df_encoded.reindex(columns=REQUIRED_FEATURES)
    
    # Final NaN handling
    df_encoded = df_encoded.fillna(0)

    logger.info(f"Batch encoding complete: output shape {df_encoded.shape}")
    logger.info(f"Column order verified: {df_encoded.columns.tolist()}")
    
    return df_encoded


def validate_batch_columns(df: pd.DataFrame) -> tuple[bool, str]:
    """
    Validate that all required columns are present in the dataframe.
    
    Args:
        df: Input dataframe to validate
        
    Returns:
        Tuple of (is_valid, message)
    """
    missing_cols = [col for col in REQUIRED_FEATURES if col not in df.columns]
    
    if missing_cols:
        error_msg = f"Missing required {len(missing_cols)} column(s): {', '.join(missing_cols[:5])}"
        if len(missing_cols) > 5:
            error_msg += f" ... and {len(missing_cols) - 5} more"
        logger.error(error_msg)
        return False, error_msg
    
    logger.info("Batch validation passed - all required columns present")
    return True, "All required columns validated"


def validate_data_types(df: pd.DataFrame) -> tuple[bool, str]:
    """
    Validate data types in the dataframe.
    
    Args:
        df: Input dataframe
        
    Returns:
        Tuple of (is_valid, message)
    """
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    object_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    if len(numeric_cols) + len(object_cols) < len(df.columns):
        return False, "Unsupported data types detected"
    
    return True, "Data types valid"

