# Telco Customer Churn Model Card

## Overview
This model estimates whether a telecom customer is likely to churn from account, billing, contract, and service attributes.

## Dataset
The training data is the Telco Customer Churn dataset with customer demographics, account tenure, subscribed services, billing method, and churn label.

## Features
The pipeline uses 19 raw input features. Categorical features are imputed and one-hot encoded; numeric features are median-imputed.

## Training Method
The model is an XGBoost classifier trained inside a scikit-learn pipeline with stratified train/test splitting and grid search.

## Hyperparameters
```json
{
  "classifier__learning_rate": 0.2,
  "classifier__max_depth": 5,
  "classifier__n_estimators": 50
}
```

## Metrics
- Accuracy: 0.7410
- Precision: 0.5080
- Recall: 0.7674
- F1: 0.6113
- ROC-AUC: 0.8347

## Limitations
The dataset is static and may not reflect current customer behavior. The model should be monitored for drift before use in a live business workflow.

## Future Improvements
Add drift detection, calibration checks, SHAP explanations, and scheduled retraining with production data snapshots.

## Training Timestamp
2026-07-04T14:53:06.352874+00:00
