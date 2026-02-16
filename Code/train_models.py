import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from xgboost import XGBClassifier

# Load the datasets
diabetes_df = pd.read_csv('Clean Datasets/diabetes_cleaned.csv')
hypertension_df = pd.read_csv('Clean Datasets/hypertension_cleaned.csv')
nafld_df = pd.read_csv('Clean Datasets/nafld_cleaned.csv')

# Handle categorical data
diabetes_df['smoking_history'] = diabetes_df['smoking_history'].astype('category').cat.codes

# 1. DIABETES MODEL (XGBoost) 
X_dia = diabetes_df[['age', 'male', 'glucose', 'bmi', 'hypertension', 'heart_disease', 'smoking_history', 'hba1c_level']]
y_dia = diabetes_df['diabetes'] 
X_train_d, X_test_d, y_train_d, y_test_d = train_test_split(X_dia, y_dia, test_size=0.2, random_state=42)

# FIX: Added scale_pos_weight=5 to handle the imbalance in diabetes cases
dia_model = XGBClassifier(eval_metric='logloss', n_estimators=100, learning_rate=0.1, scale_pos_weight=5)
dia_model.fit(X_train_d, y_train_d)

joblib.dump(dia_model, 'diabetes_model.joblib')

#  2. HYPERTENSION MODEL (Random Forest) 
X_hyp = hypertension_df[['age', 'male', 'currentsmoker', 'cigsperday', 'bpmeds', 'diabetes', 'totchol', 'sysbp', 'diabp', 'bmi', 'heartrate', 'glucose']]
y_hyp = hypertension_df['risk']
X_train_h, X_test_h, y_train_h, y_test_h = train_test_split(X_hyp, y_hyp, test_size=0.2, random_state=42)

# Added class_weight='balanced'
hyp_model = RandomForestClassifier(n_estimators=100, class_weight='balanced')
hyp_model.fit(X_train_h, y_train_h)

joblib.dump(hyp_model, 'hypertension_model.joblib')

#  3. NAFLD MODEL (Random Forest) 
X_naf = nafld_df[['age', 'male', 'bmi']]
y_naf = nafld_df['status']
X_train_n, X_test_n, y_train_n, y_test_n = train_test_split(X_naf, y_naf, test_size=0.2, random_state=42)

# Added class_weight='balanced' to improve that low 0.20 recall
naf_model = RandomForestClassifier(n_estimators=100, class_weight='balanced')
naf_model.fit(X_train_n, y_train_n)

joblib.dump(naf_model, 'nafld_model.joblib')

print("\n[1] DIABETES MODEL VALIDATION")
print(classification_report(y_test_d, dia_model.predict(X_test_d)))

print("\n[2] HYPERTENSION MODEL VALIDATION")
print(classification_report(y_test_h, hyp_model.predict(X_test_h)))

print("\n[3] NAFLD MODEL VALIDATION")
print(classification_report(y_test_n, naf_model.predict(X_test_n)))

print("\nAll balanced models trained and exported successfully!")