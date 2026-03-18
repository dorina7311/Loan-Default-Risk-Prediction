# Loan Default Risk Prediction System - Project Guide

## Overview

This is a machine learning project that predicts loan default risk. The system analyzes 16 borrower characteristics and calculates the probability that a borrower will default on their loan.

## Project Workflow

### Input
16 borrower characteristics including:
- Age, Income, Credit Score
- Loan Amount, Interest Rate
- Employment history, Debt ratios
- Education level, Marital status
- Additional financial indicators

### Processing
The trained model:
1. Analyzes all 16 borrower characteristics
2. Compares them against 255,347 historical loan records
3. Identifies patterns from borrowers who defaulted vs. who repaid
4. Calculates the probability of default

### Output
- Risk Level (Low / Medium / High)
- Probability percentage (e.g., 25.5% chance of default)
- Recommendation (Approve / Decline / Consider)

## Running the Demo

### Command
```
python demo.py
```

### Interactive Menu Options
1. View Low-Risk Borrower Example
2. View High-Risk Borrower Example  
3. View Medium-Risk Borrower Example
4. Enter Custom Borrower Data
5. View Feature Information
6. Exit

## Example Outputs

### Low-Risk Borrower
```
Age: 50
Income: $150,000
Credit Score: 800
Loan Amount: $300,000
Debt-to-Income Ratio: 0.20

Probability of Default: 8.30%
Probability of No Default: 91.70%

RECOMMENDATION: APPROVE LOAN
```

### High-Risk Borrower
```
Age: 28
Income: $35,000
Credit Score: 580
Loan Amount: $300,000
Debt-to-Income Ratio: 0.72

Probability of Default: 65.40%
Probability of No Default: 34.60%

RECOMMENDATION: DECLINE LOAN
```

## Custom Input Process

When entering custom borrower data, the system:
1. Loads the trained model from disk (138 KB)
2. Processes the 16 input features
3. Normalizes numerical features
4. Generates predictions using the trained model
5. Returns risk assessment with probability scores

## Project Components

### Data Preprocessing (data_preprocessing.py)
- Loads 255,347 loan records
- Cleans and encodes categorical variables
- Splits data into training (80%) and testing (20%) sets

### Model Training (train_model.py)
- Trains three candidate models:
  - Logistic Regression: 88.59% accuracy
  - Random Forest: 88.68% accuracy
  - Gradient Boosting: 88.73% accuracy (selected)
- Compares model performance
- Saves best model to disk

### Model Evaluation (evaluate_model.py)
- Tests model on 51,070 test samples
- Calculates performance metrics
- Generates confusion matrices and ROC curves
- Produces detailed evaluation reports

### Prediction Engine (predict.py)
- Loads trained model for inference
- Supports single and batch predictions
- Applies learned feature scaling
- Returns predictions with probability estimates

### Interactive Demo (demo.py)
- Command-line interface
- Pre-configured example profiles
- Accepts custom borrower information
- Displays risk assessments with recommendations

## Model Performance

```
Dataset: 255,347 total loan records
Training set: 204,277 samples
Test set: 51,070 samples

Selected Model: Gradient Boosting Classifier

Test Accuracy: 88.73%
Precision: 0.657
Recall: 0.052
F1-Score: 0.096
ROC-AUC: 0.757
```

Note: Low recall reflects class imbalance in data (88.3% no default, 11.7% default).

## What the System Does With Input

When a borrower's information is provided:

1. The system loads the trained Gradient Boosting model
2. Each of the 16 input features is processed and normalized
3. The model generates a prediction probability between 0 and 1
4. Based on the probability, a risk level is assigned
5. The system returns:
   - Predicted class (Default / No Default)
   - Probability of default (percentage)
   - Probability of no default (percentage)
   - Recommendation for loan decision

## Project Artifacts

| File | Purpose |
|------|---------|
| demo.py | Interactive demonstration interface |
| src/train_model.py | Model training pipeline |
| src/evaluate_model.py | Model evaluation and metrics |
| src/predict.py | Production prediction engine |
| src/data_preprocessing.py | Data preparation |
| models/loan_default_model.pkl | Trained model (saved) |
| outputs/figures/confusion_matrix_BestModel.png | Performance visualization |
| outputs/figures/roc_curve_BestModel.png | Discrimination ability chart |
| outputs/reports/evaluation_report_BestModel.txt | Detailed metrics report |
| notebooks/eda.ipynb | Exploratory data analysis |
| README.md | Full documentation |

## Complete Workflow

1. Data Collection and Loading
2. Data Preprocessing (cleaning, encoding, splitting)
3. Model Training (three algorithms tested)
4. Model Evaluation (metrics and visualizations)
5. Model Selection (best performing model saved)
6. Production Ready - Predictions on new borrowers
7. Interactive Demo for end users

## Key Technical Skills Demonstrated

- Data preprocessing and feature engineering
- Multiple machine learning algorithm implementation
- Model evaluation and comparison
- Python object-oriented design and modular architecture
- Production code with error handling and logging
- Scikit-learn library implementation
- Data visualization and reporting

## Frequently Asked Questions

### What does this project do?
The system predicts loan default risk using machine learning. It trains on historical loan data to learn patterns of borrowers who default versus those who repay. When given new borrower information, it calculates the probability of default and provides a recommendation for loan approval decisions.

### What happens when I input borrower data?
The system processes the 16 input features through a trained Gradient Boosting model and returns a prediction with accompanying probability scores and a risk assessment recommendation for loan decision making.

### Why does the model achieve 88.73% accuracy?
The model was trained on 255,347 loan records with balanced features and optimized hyperparameters. The Gradient Boosting algorithm proved most effective for this classification task compared to Logistic Regression and Random Forest.

### What limitations exist?
The model shows low recall (5.2%) due to class imbalance in the data (only 11.7% of loans actually default). This means the model is conservative in predicting defaults. Advanced techniques like SMOTE or threshold adjustment could address this in future iterations.
