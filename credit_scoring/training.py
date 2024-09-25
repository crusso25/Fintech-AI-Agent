# training.py

import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split, GridSearchCV
from imblearn.over_sampling import SMOTE
import xgboost as xgb
import joblib
import numpy as np
import os

df = pd.read_csv('data/credit_risk_dataset.csv')
print(df.head())
df = df.dropna()

# Convert categorical variables to appropriate data types
categorical_features = ['person_home_ownership', 'loan_intent', 'loan_grade']
numerical_features = [
    'person_age', 'person_income', 'person_emp_length',
    'loan_amnt', 'loan_int_rate', 'loan_percent_income',
    'cb_person_cred_hist_length'
]

for col in categorical_features:
    df[col] = df[col].astype('category')

X = df[categorical_features + numerical_features]
y = df['loan_status']

# Preprocess
encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
X_encoded = pd.DataFrame(encoder.fit_transform(X[categorical_features]))
X_encoded.columns = encoder.get_feature_names_out(categorical_features)
X_encoded.index = X.index

scaler = StandardScaler()
X_numerical = pd.DataFrame(scaler.fit_transform(X[numerical_features]), columns=numerical_features, index=X.index)
X_processed = pd.concat([X_numerical, X_encoded], axis=1)

smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_processed, y)
X_train, X_test, y_train, y_test = train_test_split(
    X_resampled, y_resampled, test_size=0.2, random_state=42
)

xgb_model = xgb.XGBClassifier(
    objective='binary:logistic',
    eval_metric='auc',
    random_state=42
)
param_grid = {
    'n_estimators': [100],
    'max_depth': [3],
    'learning_rate': [0.1],
    'subsample': [0.8]
}

grid_search = GridSearchCV(
    estimator=xgb_model,
    param_grid=param_grid,
    scoring='roc_auc',
    cv=3,
    n_jobs=-1,
    verbose=1
)

grid_search.fit(X_train, y_train)

# Best model
best_model = grid_search.best_estimator_

# Save model
if not os.path.exists('models'):
    os.makedirs('models')

joblib.dump(best_model, 'models/credit_model.pkl')
joblib.dump(scaler, 'models/scaler.pkl')
joblib.dump(encoder, 'models/encoder.pkl')

print("Model and preprocessing objects have been saved in the 'models' directory.")
