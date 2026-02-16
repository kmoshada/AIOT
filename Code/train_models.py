import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier

diabetes_df = pd.read_csv('Clean Datasets/diabetes_cleaned.csv')
hypertension_df = pd.read_csv('Clean Datasets/hypertension_cleaned.csv')
nafld_df = pd.read_csv('Clean Datasets/nafld_cleaned.csv')

diabetes_df['smoking_history'] = diabetes_df['smoking_history'].astype('category').cat.codes

X_dia = diabetes_df[['age', 'male', 'glucose', 'bmi', 'hypertension', 'heart_disease', 'smoking_history', 'hba1c_level']]
y_dia = diabetes_df['diabetes'] 

X_train_d, X_test_d, y_train_d, y_test_d = train_test_split(X_dia, y_dia, test_size=0.2, random_state=42)

# Using XGBClassifier for better accuracy with more features
dia_model = XGBClassifier(eval_metric='logloss', n_estimators=100, learning_rate=0.1)
dia_model.fit(X_train_d, y_train_d)
print(f"Diabetes Accuracy : {accuracy_score(y_test_d, dia_model.predict(X_test_d)):.2f}")

joblib.dump(dia_model, 'diabetes_model.joblib')


X_hyp = hypertension_df[['age', 'male', 'currentsmoker', 'cigsperday', 'bpmeds', 'diabetes', 'totchol', 'sysbp', 'diabp', 'bmi', 'heartrate', 'glucose']]
y_hyp = hypertension_df['risk']
X_train_h, X_test_h, y_train_h, y_test_h = train_test_split(X_hyp, y_hyp, test_size=0.2, random_state=42)

hyp_model = RandomForestClassifier(n_estimators=100)
hyp_model.fit(X_train_h, y_train_h)
print(f"Hypertension Accuracy: {accuracy_score(y_test_h, hyp_model.predict(X_test_h)):.2f}")
joblib.dump(hyp_model, 'hypertension_model.joblib')

X_naf = nafld_df[['age', 'male', 'bmi']]
y_naf = nafld_df['status']
X_train_n, X_test_n, y_train_n, y_test_n = train_test_split(X_naf, y_naf, test_size=0.2, random_state=42)

naf_model = RandomForestClassifier(n_estimators=100)
naf_model.fit(X_train_n, y_train_n)
print(f"NAFLD Accuracy: {accuracy_score(y_test_n, naf_model.predict(X_test_n)):.2f}")
joblib.dump(naf_model, 'nafld_model.joblib')

print("\nAll models trained and exported successfully!")