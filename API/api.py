from fastapi import FastAPI
from pydantic import BaseModel
import sklearn 
import joblib

path_model01 = 'Modules/diabetes_model.joblib'
path_model02 = "Modules/hypertension_model.joblib"
path_model03 = 'Modules/nafld_model.joblib'

model01 = model02 = model03 = None

print("Loading models...")

print("+-----------------------------------------------------------------------+")
try:
    model01 = joblib.load(path_model01)
    print("|  diabetes model is loaded       |")

except Exception as e:
    print(f"Warning: Error loading diabetes_model.joblib: {e}")

print("+-----------------------------------------------------------------------+")

try:
    model02 = joblib.load(path_model02)
    print("|  hypertension model is loaded   |")

except Exception as e:
    print(f"Warning: Error loading hypertension_model.joblib: {e}")

print("+-----------------------------------------------------------------------+")

try:
    model03 = joblib.load(path_model03)
    print("|  nafld model is loaded          |")
except Exception as e:
    print(f"Warning: Error loading nafld_model.joblib: {e}")

print("+-----------------------------------------------------------------------+")

class Prediction(BaseModel):
    gender: int
    age: int
    currentSmoker: int
    cigsPerDay: float
    BPMeds: int
    diabetes: int
    totChol: float
    sysBP: float
    diaBP: float
    BMI: float
    heartRate: float
    glucose: float

app = FastAPI()

@app.get("/")
def read():
    return {"Hello": "World"}

@app.post("/predict")
def predict(data: Prediction):

    results = {}

    if model01:
        diabetes_features = [[data.age, data.gender,data.glucose]]
        pred01 = model01.predict(diabetes_features)
        results["Diabetes"] = pred01[0].item()
    else:
        results["Diabetes"] = "Error loading diabetes_model"

    if model02:
        hypertension_features = [[
            data.gender, data.age, data.currentSmoker, data.cigsPerDay,
            data.BPMeds, data.diabetes, data.totChol, data.sysBP, data.diaBP,
            data.BMI, data.heartRate, data.glucose
        ]]
        pred02 = model02.predict(hypertension_features)
        results["Hypertension"] = pred02[0].item()
    else:
        results["Hypertension"] = "Error loading hypertension_model"

    if model03:
        nfld_features = [[data.age, data.gender, data.BMI]]
        pred03 = model03.predict(nfld_features)
        results["NFLD"] = pred03[0].item()
    else:
        results["NFLD"] = "Error loading nafld_model"

    return results

if __name__ == "__main__":
    import uvicorn


    uvicorn.run(app, host="0.0.0.0", port=8000)