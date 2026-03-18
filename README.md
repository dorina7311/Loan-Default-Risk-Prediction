# Loan Default Risk Prediction- Classification

## Project Overview

This is a machine learning project** for predicting the probability of loan default. The project demonstrates industry-standard practices for building, training, evaluating, and deploying classification models.

**Objective**: Classify borrowers as likely to default or not default on their loans using machine learning classification algorithms.

## Dataset Description

**Source**: `data/raw/Loan_default.csv`

**Size**: 255,347 loan records with 18 features

**Train-Test Split**: 80% training (204,277 samples), 20% testing (51,070 samples)

### Features:
- **Age**: Age of the borrower (years)
- **Income**: Annual income (USD)
- **LoanAmount**: Amount of the loan (USD)
- **CreditScore**: Credit score of the borrower (300-850)
- **MonthsEmployed**: Months of employment at current job
- **NumCreditLines**: Number of active credit lines
- **InterestRate**: Interest rate on the loan (%)
- **LoanTerm**: Length of loan (months)
- **DTIRatio**: Debt-to-Income ratio
- **Education**: Level of education (categorical)
- **EmploymentType**: Type of employment (categorical)
- **MaritalStatus**: Marital status (categorical)
- **HasMortgage**: Whether borrower has a mortgage (binary)
- **HasDependents**: Whether borrower has dependents (binary)
- **LoanPurpose**: Purpose of the loan (categorical)
- **HasCoSigner**: Whether loan has a co-signer (binary)
- **LoanID**: Unique loan identifier (dropped in preprocessing)

### Target Variable:
- **Default**: Binary classification (0 = No Default, 1 = Default)

## Project Structure

```
Loan Default Prediction/
│
├── data/
│   ├── raw/
│   │   └── Loan_default.csv          # Original dataset
│   └── processed/
│       └── cleaned_data.csv          # Processed dataset (generated)
│
├── notebooks/
│   └── eda.ipynb                     # Exploratory Data Analysis & Visualizations
│
├── src/
│   ├── data_preprocessing.py         # Data loading, cleaning, preprocessing
│   ├── train_model.py                # Model training & comparison
│   ├── evaluate_model.py             # Model evaluation & visualization
│   └── predict.py                    # Making predictions on new data
│
├── models/
│   └── loan_default_model.pkl        # Saved best model (generated)
│
├── outputs/
│   ├── figures/                      # Generated visualizations
│   │   ├── default_distribution.png
│   │   ├── correlation_heatmap.png
│   │   ├── income_credit_analysis.png
│   │   ├── feature_importance.png
│   │   └── confusion_matrix_*.png
│   └── reports/
│       └── evaluation_report_*.txt   # Model evaluation reports
│
├── requirements.txt                  # Python dependencies
├── README.md                         # This file
├── COMMANDS.md                       # Running commands and documentation
└── .gitignore                        # Git ignore file
```

## Model Performance

### Current Best Model: **Gradient Boosting**

| Metric | Value |
|--------|-------|
| Test Accuracy | 88.73% |
| Precision | 0.657 |
| Recall | 0.052 |
| F1-Score | 0.096 |
| ROC-AUC | 0.757 |

### Models Trained & Compared:
1. **Logistic Regression** - 88.59% test accuracy
2. **Random Forest** - 88.68% test accuracy
3. **Gradient Boosting** - 88.73% test accuracy ⭐ BEST

## Key Features

**Modular Architecture** - Separate modules for preprocessing, training, evaluation, and prediction

**Production-Ready Code** - Logging, error handling, and best practices throughout

**Multiple Models** - Compares Logistic Regression, Random Forest, and Gradient Boosting

*Comprehensive Evaluation** - Accuracy, precision, recall, F1-score, confusion matrix, ROC curve

**Visualization Suite** - 5+ detailed plots including correlations, distributions, and feature importance

**Prediction Pipeline** - Easy-to-use interface for making predictions on new borrowers

**Documentation** - Detailed README, inline comments, and example usage

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Step 1: Clone/Download the Project
```bash
cd "Loan Default Prediction"
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### 1. **Run Complete EDA & Visualizations**
```bash
jupyter notebook notebooks/eda.ipynb
```
Explore the dataset, view visualizations, and understand data patterns.

### 2. **Train Models**
```bash
python src/train_model.py
```
This will:
- Load and preprocess data
- Train Logistic Regression, Random Forest, and Gradient Boosting
- Compare model performances
- Save the best model to `models/loan_default_model.pkl`

### 3. **Evaluate the Best Model**
```bash
python src/evaluate_model.py
```
This will:
- Load the trained model
- Generate evaluation metrics
- Create confusion matrix and ROC curve plots
- Save evaluation reports

### 4. **Make Predictions on New Data**
```bash
python src/predict.py
```

**Example: Single Borrower Prediction**
```python
from src.predict import LoanDefaultPredictor

predictor = LoanDefaultPredictor('models/loan_default_model.pkl')

# Sample borrower
borrower = {
    'Age': 35,
    'Income': 75000,
    'LoanAmount': 250000,
    'CreditScore': 720,
    # ... other features
}

result = predictor.predict_single(borrower)
print(f"Prediction: {result['prediction_label']}")
print(f"Probability of Default: {result['probability_default']:.4f}")
```

**Example: Batch Predictions**
```python
import pandas as pd

# Load borrowers from CSV or create DataFrame
borrowers_df = pd.read_csv('borrowers.csv')

# Make batch predictions
results = predictor.predict_batch(borrowers_df)
print(results)
```

## Key Insights from EDA

### Class Balance
- **No Default**: 88.3% of loans (225,565 samples)
- **Default**: 11.7% of loans (29,782 samples)

### Important Features (by importance)
1. **CreditScore** - Strongest predictor of default (negative correlation: -0.45)
2. **DTIRatio** - Debt-to-income ratio significantly impacts default (positive correlation: +0.38)
3. **Income** - Higher income correlates with lower default risk (negative correlation: -0.32)
4. **InterestRate** - Higher rates correlate with higher default probability
5. **LoanAmount** - Larger loans slightly increase default risk

### Correlations with Default
- **CreditScore**: -0.45 (strong negative - higher credit score = lower default)
- **DTIRatio**: +0.38 (positive - higher debt ratio = higher default)
- **Income**: -0.32 (negative - higher income = lower default)

## Model Features & Capabilities

### Preprocessing Pipeline
- Automatic categorical encoding with LabelEncoder
- Feature scaling with StandardScaler
- Automatic missing value detection
- Feature normalization

### Training Module
- Multiple algorithm comparison
- Hyperparameter tuning ready
- Cross-validation support
- Model serialization (pickle)

### Prediction Module
- Single borrower predictions
- Batch predictions from DataFrame
- Probability estimates

## Performance Optimization Tips

### Improving Recall (Catching More Defaults)
```python
# Adjust decision threshold
y_pred_proba = model.predict_proba(X_test)[:, 1]
y_pred_adjusted = (y_pred_proba > 0.3).astype(int)  # Lower threshold
```

### Handling Class Imbalance
```python
from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
```

### Hyperparameter Tuning
```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [10, 20, None]
}

grid_search = GridSearchCV(model, param_grid, cv=5)
grid_search.fit(X_train, y_train)
```


## References

- Scikit-learn Documentation: https://scikit-learn.org/
- Pandas Documentation: https://pandas.pydata.org/
- Machine Learning Best Practices: https://developers.google.com/machine-learning/guides

