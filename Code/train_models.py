import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score

diabetes_df = pd.read_csv('Clean Datasets/diabetes_cleaned.csv')
hypertension_df = pd.read_csv('Clean Datasets/hypertension_cleaned.csv')
nafld_df = pd.read_csv('Clean Datasets/nafld_cleaned.csv')

diabetes_df['smoking_history'] = diabetes_df['smoking_history'].astype('category').cat.codes

X_dia = diabetes_df[['age', 'male', 'glucose', 'bmi', 'hypertension', 'heart_disease', 'smoking_history', 'hba1c_level']]
y_dia = diabetes_df['diabetes'] 
X_train_d, X_test_d, y_train_d, y_test_d = train_test_split(X_dia, y_dia, test_size=0.2, random_state=42)

dia_model = XGBClassifier(eval_metric='logloss', scale_pos_weight=5)
dia_model.fit(X_train_d, y_train_d)
joblib.dump(dia_model, 'diabetes_model.joblib')

X_hyp = hypertension_df[['age', 'male', 'currentsmoker', 'cigsperday', 'bpmeds', 'diabetes', 'totchol', 'sysbp', 'diabp', 'bmi', 'heartrate', 'glucose']]
y_hyp = hypertension_df['risk']
X_train_h, X_test_h, y_train_h, y_test_h = train_test_split(X_hyp, y_hyp, test_size=0.2, random_state=42)

hyp_model = RandomForestClassifier(n_estimators=100, class_weight='balanced')
hyp_model.fit(X_train_h, y_train_h)
joblib.dump(hyp_model, 'hypertension_model.joblib')

X_naf = nafld_df[['age', 'male', 'bmi', 'glucose', 'hypertension', 'diabetes']]
y_naf = nafld_df['fibrosis_status'] 
X_train_n, X_test_n, y_train_n, y_test_n = train_test_split(X_naf, y_naf, test_size=0.2, random_state=42)

naf_model = RandomForestClassifier(n_estimators=100, class_weight='balanced')
naf_model.fit(X_train_n, y_train_n)
joblib.dump(naf_model, 'nafld_model.joblib')

models = [('Diabetes', dia_model, X_test_d, y_test_d), 
          ('Hypertension', hyp_model, X_test_h, y_test_h), 
          ('NAFLD (Fibrosis)', naf_model, X_test_n, y_test_n)]

print("METABOLIC RISK DETECTION SYSTEM: FINAL EVALUATION")

for name, model, X_test, y_test in models:
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    print(f"\n{name.upper()} MODEL PERFORMANCE")
    print(f"Overall Accuracy Score: {acc:.4f}") 
    print(classification_report(y_test, y_pred))

print("SUCCESS: Triple-Pipeline Synchronization Complete.")
print("All optimized .joblib models exported ")
