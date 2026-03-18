# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. **Install Dependencies**
```bash
source venv/bin/activate  # Activate virtual environment
pip install -r requirements.txt
```

### 2. **Train Models**
```bash
python src/train_model.py
```
✅ This will:
- Load and preprocess the loan data
- Train 3 models: Logistic Regression, Random Forest, Gradient Boosting
- Compare performances
- Save the best model to `models/loan_default_model.pkl`

**Expected Output:**
```
GradientBoosting - Test Accuracy: 0.8873
Best Model: GradientBoosting
Model saved to models/loan_default_model.pkl
```

### 3. **Evaluate the Model**
```bash
python src/evaluate_model.py
```
✅ This will:
- Load the trained model
- Generate evaluation metrics (accuracy, precision, recall, F1)
- Create confusion matrix visualization
- Create ROC curve plot
- Save evaluation report

**Output Files:**
- `outputs/figures/confusion_matrix_BestModel.png`
- `outputs/figures/roc_curve_BestModel.png`
- `outputs/reports/evaluation_report_BestModel.txt`

### 4. **Make Predictions**
```bash
python src/predict.py
```

Or use predictions in your code:
```python
from src.predict import LoanDefaultPredictor

# Load predictor
predictor = LoanDefaultPredictor('models/loan_default_model.pkl')

# Predict for single borrower
borrower_data = {
    'Age': 35,
    'Income': 75000,
    'LoanAmount': 250000,
    'CreditScore': 720,
    # ... other features
}

result = predictor.predict_single(borrower_data)
print(f"Risk: {result['prediction_label']}")
print(f"Default Probability: {result['probability_default']:.2%}")
```

### 5. **View EDA & Visualizations**
```bash
jupyter notebook notebooks/eda.ipynb
```

---

## 📊 Project Architecture

```
src/
├── data_preprocessing.py      ← Data loading & cleaning
├── train_model.py              ← Model training
├── evaluate_model.py           ← Model evaluation
└── predict.py                  ← Predictions

Input: data/raw/Loan_default.csv
Output: models/loan_default_model.pkl
        outputs/figures/*.png
        outputs/reports/*.txt
```

---

## 📈 Model Performance

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| Logistic Regression | 88.59% | 0.620 | 0.031 | 0.059 |
| Random Forest | 88.68% | 0.638 | 0.047 | 0.087 |
| **Gradient Boosting** | **88.73%** | **0.657** | **0.052** | **0.096** |

**Best Model: Gradient Boosting with 88.73% test accuracy**

---

## 🔧 Each Module Explained

### `data_preprocessing.py`
- Loads CSV data
- Drops non-useful columns (LoanID)
- Encodes categorical variables
- Performs 80-20 train-test split
- Returns: `X_train`, `X_test`, `y_train`, `y_test`

**Usage:**
```python
from src.data_preprocessing import preprocess_pipeline
result = preprocess_pipeline("data/raw/Loan_default.csv")
```

### `train_model.py`
- Trains multiple algorithms
- Compares model performances
- Selects best model
- Saves to pickle file

**Usage:**
```python
from src.train_model import train_all_models
trainer, model, comparison = train_all_models(
    X_train, X_test, y_train, y_test
)
```

### `evaluate_model.py`
- Loads saved model
- Calculates metrics
- Creates visualizations
- Generates reports

**Usage:**
```python
from src.evaluate_model import evaluate_model
evaluator = evaluate_model(model, X_test, y_test)
```

### `predict.py`
- Makes predictions on new data
- Handles single & batch predictions
- Returns predictions + probabilities

**Usage:**
```python
from src.predict import LoanDefaultPredictor
predictor = LoanDefaultPredictor('models/loan_default_model.pkl')
result = predictor.predict_single(features)
```

---

## 📁 Output Files Generated

After running `evaluate_model.py`, you'll get:

**Visualizations** (`outputs/figures/`):
- `confusion_matrix_BestModel.png` - Shows true vs predicted labels
- `roc_curve_BestModel.png` - Shows ROC curve and AUC score

**Reports** (`outputs/reports/`):
- `evaluation_report_BestModel.txt` - Detailed evaluation metrics

**Model** (`models/`):
- `loan_default_model.pkl` - Serialized trained model

---

## 🎯 Common Use Cases

### Use Case 1: Risk Assessment for New Loan Application
```python
from src.predict import LoanDefaultPredictor
import pandas as pd

predictor = LoanDefaultPredictor('models/loan_default_model.pkl')

applicant = {
    'Age': 45, 'Income': 95000, 'LoanAmount': 300000,
    'CreditScore': 750, 'MonthsEmployed': 240, 'NumCreditLines': 6,
    'InterestRate': 4.5, 'LoanTerm': 360, 'DTIRatio': 0.32,
    'Education': 2, 'EmploymentType': 1, 'MaritalStatus': 1,
    'HasMortgage': 1, 'HasDependents': 1, 'LoanPurpose': 0,
    'HasCoSigner': 0
}

risk = predictor.predict_single(applicant)
if risk['probability_default'] > 0.5:
    print("⚠️ HIGH RISK - Decline application")
elif risk['probability_default'] > 0.3:
    print("⚠️ MEDIUM RISK - Request additional verification")
else:
    print("✅ LOW RISK - Approve application")
```

### Use Case 2: Batch Scoring Portfolio
```python
portfolio = pd.read_csv('loan_portfolio.csv')
predictions = predictor.predict_batch(portfolio)

# Identify high-risk loans
high_risk = predictions[predictions['probability_default'] > 0.5]
print(f"High-risk loans: {len(high_risk)} / {len(predictions)}")
```

---

## ⚙️ Troubleshooting

**Issue: `FileNotFoundError`**
- Make sure you're in the project root directory
- Check that `data/raw/Loan_default.csv` exists

**Issue: Model loading fails**
- Ensure the model file exists at `models/loan_default_model.pkl`
- Run `train_model.py` first to generate the model

**Issue: Low recall (missing defaults)**
- Consider adjusting the prediction threshold
- Try using class weights or SMOTE for imbalanced data

---

## 📚 Next Steps for Production

1. **API Development**: Wrap the predictor in Flask/FastAPI
2. **Database**: Store predictions and feedback
3. **Monitoring**: Track model performance over time
4. **Retraining**: Automate model updates as new data arrives
5. **CI/CD**: Automated testing and deployment pipeline

---

## 📞 Support

For detailed documentation, see:
- `README.md` - Complete project documentation
- `notebooks/eda.ipynb` - Data exploration and analysis
- Source code comments - Implementation details
