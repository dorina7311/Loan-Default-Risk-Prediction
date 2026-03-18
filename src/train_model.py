import pandas as pd
import numpy as np
import logging
import pickle
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import GridSearchCV
from imblearn.over_sampling import SMOTE
import warnings

warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ModelTrainer:
    """
    Class to train and evaluate multiple ML models.
    Implements best practices: SMOTE, hyperparameter tuning, cross-validation.
    """
    
    def __init__(self, random_state=42, use_smote=True):
        """Initialize ModelTrainer."""
        self.random_state = random_state
        self.use_smote = use_smote
        self.models = {}
        self.results = {}
        self.scaler = StandardScaler()
        self.best_model = None
        self.best_model_name = None
        
    def _apply_smote(self, X_train, y_train):
        """Apply SMOTE to handle class imbalance."""
        if not self.use_smote:
            return X_train, y_train
        
        logger.info("Applying SMOTE for class imbalance handling...")
        smote = SMOTE(random_state=self.random_state, k_neighbors=5)
        X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
        
        logger.info(f"Original class distribution: {np.bincount(y_train)}")
        logger.info(f"Balanced class distribution: {np.bincount(y_train_balanced)}")
        
        return X_train_balanced, y_train_balanced
        
    def _scale_data(self, X_train, X_test):
        """Scale features using StandardScaler."""
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        logger.info("Features scaled using StandardScaler")
        return X_train_scaled, X_test_scaled
    
    def train_logistic_regression(self, X_train, X_test, y_train, y_test, scale=True):
        """Train Logistic Regression model with SMOTE."""
        logger.info("Training Logistic Regression...")
        
        X_train_use, X_test_use = (self._scale_data(X_train, X_test) if scale 
                                   else (X_train.values, X_test.values))
        
        # Apply SMOTE for class imbalance
        X_train_balanced, y_train_balanced = self._apply_smote(X_train_use, y_train)
        
        model = LogisticRegression(
            random_state=self.random_state,
            max_iter=1000,
            class_weight='balanced'
        )
        model.fit(X_train_balanced, y_train_balanced)
        
        # Predictions
        y_train_pred = model.predict(X_train_balanced)
        y_test_pred = model.predict(X_test_use)
        
        # Metrics
        metrics = self._calculate_metrics(y_train_balanced, y_train_pred, y_test, y_test_pred)
        
        self.models['LogisticRegression'] = model
        self.results['LogisticRegression'] = metrics
        
        logger.info(f"Logistic Regression - Test Accuracy: {metrics['test_accuracy']:.4f}")
        return model, metrics
    
    def train_random_forest(self, X_train, X_test, y_train, y_test, scale=False, 
                           n_estimators=150):
        """Train Random Forest model with SMOTE."""
        logger.info("Training Random Forest...")
        
        X_train_use = X_train.values if isinstance(X_train, pd.DataFrame) else X_train
        X_test_use = X_test.values if isinstance(X_test, pd.DataFrame) else X_test
        
        # Apply SMOTE for class imbalance
        X_train_balanced, y_train_balanced = self._apply_smote(X_train_use, y_train)
        
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=15,
            min_samples_split=20,
            class_weight='balanced',
            random_state=self.random_state,
            n_jobs=-1,
            verbose=0
        )
        model.fit(X_train_balanced, y_train_balanced)
        
        # Predictions
        y_train_pred = model.predict(X_train_balanced)
        y_test_pred = model.predict(X_test_use)
        
        # Metrics
        metrics = self._calculate_metrics(y_train_balanced, y_train_pred, y_test, y_test_pred)
        
        self.models['RandomForest'] = model
        self.results['RandomForest'] = metrics
        
        logger.info(f"Random Forest - Test Accuracy: {metrics['test_accuracy']:.4f}")
        return model, metrics
    
    def train_gradient_boosting(self, X_train, X_test, y_train, y_test, scale=False):
        """Train optimized Gradient Boosting model with hyperparameter tuning."""
        logger.info("Training Gradient Boosting with optimization...")
        
        X_train_use = X_train.values if isinstance(X_train, pd.DataFrame) else X_train
        X_test_use = X_test.values if isinstance(X_test, pd.DataFrame) else X_test
        
        # Apply SMOTE for class imbalance
        X_train_balanced, y_train_balanced = self._apply_smote(X_train_use, y_train)
        
        # Define parameter grid for tuning
        param_grid = {
            'n_estimators': [150, 200],
            'learning_rate': [0.05, 0.1],
            'max_depth': [5, 7],
            'min_samples_split': [20, 30],
            'subsample': [0.8, 0.9]
        }
        
        # Base model with good hyperparameters
        gb_base = GradientBoostingClassifier(
            random_state=self.random_state,
            verbose=0
        )
        
        # GridSearchCV for hyperparameter tuning
        logger.info("Running GridSearchCV for hyperparameter optimization...")
        grid_search = GridSearchCV(
            gb_base,
            param_grid,
            cv=5,
            scoring='accuracy',
            n_jobs=-1,
            verbose=0
        )
        
        grid_search.fit(X_train_balanced, y_train_balanced)
        model = grid_search.best_estimator_
        
        logger.info(f"Best parameters: {grid_search.best_params_}")
        logger.info(f"Best CV accuracy: {grid_search.best_score_:.4f}")
        
        # Predictions
        y_train_pred = model.predict(X_train_balanced)
        y_test_pred = model.predict(X_test_use)
        
        # Metrics
        metrics = self._calculate_metrics(y_train_balanced, y_train_pred, y_test, y_test_pred)
        
        self.models['GradientBoosting'] = model
        self.results['GradientBoosting'] = metrics
        
        logger.info(f"Gradient Boosting - Test Accuracy: {metrics['test_accuracy']:.4f}")
        return model, metrics
    
    def _calculate_metrics(self, y_train, y_train_pred, y_test, y_test_pred):
        """Calculate evaluation metrics."""
        return {
            'train_accuracy': accuracy_score(y_train, y_train_pred),
            'train_precision': precision_score(y_train, y_train_pred),
            'train_recall': recall_score(y_train, y_train_pred),
            'train_f1': f1_score(y_train, y_train_pred),
            'test_accuracy': accuracy_score(y_test, y_test_pred),
            'test_precision': precision_score(y_test, y_test_pred),
            'test_recall': recall_score(y_test, y_test_pred),
            'test_f1': f1_score(y_test, y_test_pred),
        }
    
    def compare_models(self):
        """Compare all trained models."""
        logger.info("\n" + "="*60)
        logger.info("MODEL COMPARISON")
        logger.info("="*60)
        
        comparison_df = pd.DataFrame(self.results).T
        logger.info("\n" + str(comparison_df))
        
        # Find best model by test accuracy
        self.best_model_name = comparison_df['test_accuracy'].idxmax()
        self.best_model = self.models[self.best_model_name]
        
        logger.info(f"\nBest Model: {self.best_model_name}")
        logger.info(f"Test Accuracy: {comparison_df.loc[self.best_model_name, 'test_accuracy']:.4f}")
        
        return comparison_df
    
    def save_model(self, filepath):
        """Save best model to disk."""
        if self.best_model is None:
            logger.error("No model trained yet!")
            return False
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        model_data = {
            'model': self.best_model,
            'model_name': self.best_model_name,
            'scaler': self.scaler
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        logger.info(f"Model saved to {filepath}")
        return True


def train_all_models(X_train, X_test, y_train, y_test, model_save_path='models/loan_default_model.pkl'):
    """
    Train all models and save the best one.
    
    Args:
        X_train, X_test: Training and testing features
        y_train, y_test: Training and testing targets
        model_save_path: Path to save the best model
        
    Returns:
        tuple: (trainer object, best model, comparison dataframe)
    """
    trainer = ModelTrainer()
    
    # Train models
    trainer.train_logistic_regression(X_train, X_test, y_train, y_test, scale=True)
    trainer.train_random_forest(X_train, X_test, y_train, y_test)
    trainer.train_gradient_boosting(X_train, X_test, y_train, y_test)
    
    # Compare models
    comparison_df = trainer.compare_models()
    
    # Save best model
    trainer.save_model(model_save_path)
    
    return trainer, trainer.best_model, comparison_df


if __name__ == "__main__":
    from data_preprocessing import preprocess_pipeline
    from pathlib import Path
    
    project_root = Path(__file__).parent.parent
    data_path = project_root / "data" / "raw" / "Loan_default.csv"
    model_path = project_root / "models" / "loan_default_model.pkl"
    
    # Load and preprocess data
    prep_result = preprocess_pipeline(str(data_path))
    X_train = prep_result['X_train']
    X_test = prep_result['X_test']
    y_train = prep_result['y_train']
    y_test = prep_result['y_test']
    
    # Train models
    trainer, best_model, comparison = train_all_models(
        X_train, X_test, y_train, y_test,
        model_save_path=str(model_path)
    )
