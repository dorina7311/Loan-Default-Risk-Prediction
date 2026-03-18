"""
Model Evaluation Module

This module handles model evaluation, metrics calculation, and visualization.
"""

import pickle
import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve,
    auc
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set style for plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


class ModelEvaluator:
    """
    Class to evaluate model performance with visualization.
    """
    
    def __init__(self, model, X_test, y_test, y_pred, model_name="Model"):
        """
        Initialize ModelEvaluator.
        
        Args:
            model: Trained model object
            X_test: Test features
            y_test: True test labels
            y_pred: Predicted labels
            model_name: Name of the model
        """
        self.model = model
        self.X_test = X_test
        self.y_test = y_test
        self.y_pred = y_pred
        self.model_name = model_name
        self.metrics = {}
    
    def calculate_metrics(self):
        """Calculate evaluation metrics."""
        logger.info(f"Calculating metrics for {self.model_name}...")
        
        self.metrics = {
            'accuracy': accuracy_score(self.y_test, self.y_pred),
            'precision': precision_score(self.y_test, self.y_pred),
            'recall': recall_score(self.y_test, self.y_pred),
            'f1_score': f1_score(self.y_test, self.y_pred),
            'confusion_matrix': confusion_matrix(self.y_test, self.y_pred),
        }
        
        # Try to calculate ROC-AUC if model supports probability predictions
        try:
            y_pred_proba = self.model.predict_proba(self.X_test)[:, 1]
            self.metrics['roc_auc'] = roc_auc_score(self.y_test, y_pred_proba)
            self.metrics['y_pred_proba'] = y_pred_proba
        except Exception as e:
            logger.warning(f"Could not calculate ROC-AUC: {str(e)}")
        
        logger.info(f"Metrics calculated successfully")
        return self.metrics
    
    def print_report(self):
        """Print detailed classification report."""
        logger.info("\n" + "="*60)
        logger.info(f"EVALUATION REPORT - {self.model_name}")
        logger.info("="*60)
        
        logger.info(f"\nAccuracy:  {self.metrics['accuracy']:.4f}")
        logger.info(f"Precision: {self.metrics['precision']:.4f}")
        logger.info(f"Recall:    {self.metrics['recall']:.4f}")
        logger.info(f"F1-Score:  {self.metrics['f1_score']:.4f}")
        
        if 'roc_auc' in self.metrics:
            logger.info(f"ROC-AUC:   {self.metrics['roc_auc']:.4f}")
        
        logger.info("\nConfusion Matrix:")
        logger.info(str(self.metrics['confusion_matrix']))
        
        logger.info("\nClassification Report:")
        report = classification_report(
            self.y_test, self.y_pred,
            target_names=['No Default', 'Default']
        )
        logger.info("\n" + report)
    
    def plot_confusion_matrix(self, save_path=None):
        """Plot confusion matrix."""
        cm = self.metrics['confusion_matrix']
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=True)
        plt.title(f'Confusion Matrix - {self.model_name}')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        
        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Confusion matrix plot saved to {save_path}")
        
        plt.show()
    
    def plot_roc_curve(self, save_path=None):
        """Plot ROC curve."""
        if 'y_pred_proba' not in self.metrics:
            logger.warning("Probability predictions not available for ROC curve")
            return
        
        y_pred_proba = self.metrics['y_pred_proba']
        fpr, tpr, thresholds = roc_curve(self.y_test, y_pred_proba)
        roc_auc = auc(fpr, tpr)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, 
                label=f'ROC curve (AUC = {roc_auc:.4f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title(f'ROC Curve - {self.model_name}')
        plt.legend(loc="lower right")
        plt.tight_layout()
        
        if save_path:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"ROC curve plot saved to {save_path}")
        
        plt.show()
    
    def save_report(self, save_path):
        """Save evaluation report to file."""
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(save_path, 'w') as f:
            f.write(f"{'='*60}\n")
            f.write(f"MODEL EVALUATION REPORT - {self.model_name}\n")
            f.write(f"{'='*60}\n\n")
            
            f.write(f"Accuracy:  {self.metrics['accuracy']:.4f}\n")
            f.write(f"Precision: {self.metrics['precision']:.4f}\n")
            f.write(f"Recall:    {self.metrics['recall']:.4f}\n")
            f.write(f"F1-Score:  {self.metrics['f1_score']:.4f}\n")
            
            if 'roc_auc' in self.metrics:
                f.write(f"ROC-AUC:   {self.metrics['roc_auc']:.4f}\n")
            
            f.write(f"\nConfusion Matrix:\n")
            f.write(str(self.metrics['confusion_matrix']) + "\n\n")
            
            f.write(f"Classification Report:\n")
            report = classification_report(
                self.y_test, self.y_pred,
                target_names=['No Default', 'Default']
            )
            f.write(report)
        
        logger.info(f"Report saved to {save_path}")


def load_model(model_path):
    """
    Load saved model from disk.
    
    Args:
        model_path (str): Path to saved model
        
    Returns:
        dict: Model data including model, scaler, etc.
    """
    try:
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        logger.info(f"Model loaded from {model_path}")
        return model_data
    except FileNotFoundError:
        logger.error(f"Model file not found: {model_path}")
        raise
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise


def evaluate_model(model, X_test, y_test, model_name="Model", plots_dir=None, report_dir=None):
    """
    Comprehensive model evaluation.
    
    Args:
        model: Trained model
        X_test: Test features
        y_test: Test labels
        model_name: Name of the model
        plots_dir: Directory to save plots
        report_dir: Directory to save reports
        
    Returns:
        ModelEvaluator: Evaluator object with metrics
    """
    # Convert to numpy if needed
    X_test_use = X_test.values if isinstance(X_test, pd.DataFrame) else X_test
    
    # Make predictions
    y_pred = model.predict(X_test_use)
    
    # Create evaluator
    evaluator = ModelEvaluator(model, X_test_use, y_test, y_pred, model_name)
    
    # Calculate metrics
    evaluator.calculate_metrics()
    
    # Print report
    evaluator.print_report()
    
    # Save visualizations
    if plots_dir:
        evaluator.plot_confusion_matrix(f"{plots_dir}/confusion_matrix_{model_name}.png")
        evaluator.plot_roc_curve(f"{plots_dir}/roc_curve_{model_name}.png")
    
    # Save report
    if report_dir:
        evaluator.save_report(f"{report_dir}/evaluation_report_{model_name}.txt")
    
    return evaluator


if __name__ == "__main__":
    # Example usage
    from data_preprocessing import preprocess_pipeline
    from pathlib import Path
    
    # Get project root directory
    project_root = Path(__file__).parent.parent
    data_path = project_root / "data" / "raw" / "Loan_default.csv"
    model_path = project_root / "models" / "loan_default_model.pkl"
    plots_dir = project_root / "outputs" / "figures"
    report_dir = project_root / "outputs" / "reports"
    
    # Load data
    prep_result = preprocess_pipeline(str(data_path))
    X_test = prep_result['X_test']
    y_test = prep_result['y_test']
    
    # Load model
    model_data = load_model(str(model_path))
    model = model_data['model']
    
    # Evaluate
    evaluator = evaluate_model(
        model, X_test, y_test,
        model_name="BestModel",
        plots_dir=str(plots_dir),
        report_dir=str(report_dir)
    )
