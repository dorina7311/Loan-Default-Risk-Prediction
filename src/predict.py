

import pickle
import pandas as pd
import numpy as np
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LoanDefaultPredictor:
    """
    Class to make predictions on new borrower data.
    """

    REQUIRED_FEATURES = [
        'Age', 'Income', 'LoanAmount', 'CreditScore', 'MonthsEmployed',
        'NumCreditLines', 'InterestRate', 'LoanTerm', 'DTIRatio',
        'Education', 'EmploymentType', 'MaritalStatus', 'HasMortgage',
        'HasDependents', 'LoanPurpose', 'HasCoSigner'
    ]
    
    def __init__(self, model_path):
        """
        Initialize predictor with saved model.
        
        Args:
            model_path (str): Path to saved model pickle file
        """
        self.model_path = model_path
        self.model_data = self._load_model()
        self.model = self.model_data['model']
        self.scaler = self.model_data.get('scaler', None)
        self.model_name = self.model_data.get('model_name', 'Unknown')
        logger.info(f"Predictor initialized with model: {self.model_name}")
    
    def _load_model(self):
        """Load model from disk."""
        try:
            with open(self.model_path, 'rb') as f:
                model_data = pickle.load(f)
            logger.info(f"Model loaded from {self.model_path}")
            return model_data
        except FileNotFoundError:
            logger.error(f"Model file not found: {self.model_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def predict_single(self, features):
        """
        Predict for a single borrower.
        
        Args:
            features (dict or array-like): Borrower features
            
        Returns:
            dict: Prediction result with probability
        """
        # Convert input to DataFrame and enforce required columns
        if isinstance(features, dict):
            feature_df = pd.DataFrame([features])
        else:
            # array-like from form input: assume values correspond to required fields order
            feature_df = pd.DataFrame([features], columns=self.REQUIRED_FEATURES) if len(np.array(features).shape) == 1 else pd.DataFrame(features)

        feature_df = feature_df.reindex(columns=self.REQUIRED_FEATURES)
        feature_df = feature_df.fillna(0)
        features_array = feature_df.values

        # StandardScaler expects the same number of features as during training
        if self.scaler is not None:
            expected_features = getattr(self.scaler, 'n_features_in_', None)
            if expected_features is not None and features_array.shape[1] != expected_features:
                raise ValueError(
                    f"Model expects {expected_features} features, but input has {features_array.shape[1]}. "
                    "Please ensure your dataset has the required columns: "
                    f"{', '.join(self.REQUIRED_FEATURES)}"
                )
            features_array = self.scaler.transform(features_array)
        
        # Make prediction
        prediction = self.model.predict(features_array)[0]
        
        # Get probability
        try:
            probability = self.model.predict_proba(features_array)[0]
            prob_no_default = probability[0]
            prob_default = probability[1]
        except:
            prob_no_default = None
            prob_default = None
        
        result = {
            'prediction': prediction,
            'prediction_label': 'Default' if prediction == 1 else 'No Default',
            'probability_no_default': prob_no_default,
            'probability_default': prob_default
        }
        
        return result
    
    def predict_batch(self, feature_list):
        """
        Predict for multiple borrowers.
        
        Args:
            feature_list (list of dict or pd.DataFrame): List of borrower features
            
        Returns:
            pd.DataFrame: Predictions for all borrowers
        """
        if isinstance(feature_list, pd.DataFrame):
            feature_df = feature_list.copy()
        else:
            feature_df = pd.DataFrame(feature_list)

        # Enforce required order and drop irrelevant columns
        missing_cols = [c for c in self.REQUIRED_FEATURES if c not in feature_df.columns]
        if missing_cols:
            logger.warning(f"Missing columns in batch input, filling with zeros: {missing_cols}")

        feature_df = feature_df.reindex(columns=self.REQUIRED_FEATURES)
        feature_df = feature_df.fillna(0)

        features_array = feature_df.values

        # StandardScaler expects the same number of features as during training
        if self.scaler is not None:
            expected_features = getattr(self.scaler, 'n_features_in_', None)
            if expected_features is not None and features_array.shape[1] != expected_features:
                raise ValueError(
                    f"Model expects {expected_features} features, but input has {features_array.shape[1]}. "
                    "Please ensure your dataset has the required columns: "
                    f"{', '.join(self.REQUIRED_FEATURES)}"
                )
            features_array = self.scaler.transform(features_array)
        
        # Make predictions
        predictions = self.model.predict(features_array)
        
        # Get probabilities
        try:
            probabilities = self.model.predict_proba(features_array)
        except:
            probabilities = None
        
        results = []
        for i, pred in enumerate(predictions):
            result = {
                'prediction': pred,
                'prediction_label': 'Default' if pred == 1 else 'No Default',
            }
            
            if probabilities is not None:
                result['probability_no_default'] = probabilities[i][0]
                result['probability_default'] = probabilities[i][1]
            
            results.append(result)
        
        return pd.DataFrame(results)


def example_single_prediction():
    """
    Example: Predict for a single borrower.
    """
    from pathlib import Path
    project_root = Path(__file__).parent.parent
    model_path = project_root / "models" / "loan_default_model.pkl"
    
    predictor = LoanDefaultPredictor(str(model_path))
    
    # Sample borrower data (must match training features in order)
    # Features: Age, Income, LoanAmount, CreditScore, MonthsEmployed, NumCreditLines,
    #           InterestRate, LoanTerm, DTIRatio, Education, EmploymentType, 
    #           MaritalStatus, HasMortgage, HasDependents, LoanPurpose, HasCoSigner
    
    sample_borrower = {
        'Age': 35,
        'Income': 75000,
        'LoanAmount': 250000,
        'CreditScore': 720,
        'MonthsEmployed': 120,
        'NumCreditLines': 5,
        'InterestRate': 5.5,
        'LoanTerm': 360,
        'DTIRatio': 0.35,
        'Education': 2,  # Encoded
        'EmploymentType': 1,
        'MaritalStatus': 0,
        'HasMortgage': 1,
        'HasDependents': 0,
        'LoanPurpose': 0,
        'HasCoSigner': 0
    }
    
    logger.info("Making prediction for sample borrower...")
    result = predictor.predict_single(sample_borrower)
    
    logger.info(f"Prediction: {result['prediction_label']}")
    if result['probability_default'] is not None:
        logger.info(f"Probability of Default: {result['probability_default']:.4f}")
        logger.info(f"Probability of No Default: {result['probability_no_default']:.4f}")
    
    return result


def example_batch_prediction():
    """
    Example: Predict for multiple borrowers.
    """
    from pathlib import Path
    project_root = Path(__file__).parent.parent
    model_path = project_root / "models" / "loan_default_model.pkl"
    
    predictor = LoanDefaultPredictor(str(model_path))
    
    # Sample borrowers (as DataFrame)
    borrowers_df = pd.DataFrame({
        'Age': [35, 45, 28],
        'Income': [75000, 120000, 55000],
        'LoanAmount': [250000, 400000, 150000],
        'CreditScore': [720, 780, 650],
        'MonthsEmployed': [120, 180, 60],
        'NumCreditLines': [5, 8, 3],
        'InterestRate': [5.5, 4.5, 6.5],
        'LoanTerm': [360, 360, 240],
        'DTIRatio': [0.35, 0.30, 0.40],
        'Education': [2, 2, 1],
        'EmploymentType': [1, 1, 0],
        'MaritalStatus': [0, 1, 0],
        'HasMortgage': [1, 1, 0],
        'HasDependents': [0, 1, 0],
        'LoanPurpose': [0, 2, 1],
        'HasCoSigner': [0, 0, 1]
    })
    
    logger.info("Making batch predictions...")
    results_df = predictor.predict_batch(borrowers_df)
    
    logger.info("\nPredictions:")
    logger.info(str(results_df))
    
    return results_df


if __name__ == "__main__":
    from pathlib import Path
    
    # Get project root directory
    project_root = Path(__file__).parent.parent
    model_path = project_root / "models" / "loan_default_model.pkl"
    
    print("\n" + "="*60)
    print("SINGLE BORROWER PREDICTION")
    print("="*60)
    single_result = example_single_prediction()
    
    print("\n" + "="*60)
    print("BATCH BORROWER PREDICTION")
    print("="*60)
    batch_results = example_batch_prediction()
