from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import joblib


model01 = joblib.load('predictor01.joblib')
model02 = joblib.load('predictor02.joblib')
model03 = joblib.load('predictor03.joblib')


""" class Diabetes(BaseModel):
    glucose: float
    age: int
    gender: int

class Hypertension(BaseModel):
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

class NFLD(BaseModel):
    age: int
    gender: int
    BMI: float """

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

     diabetes_features = [[
         data.glucose,
         data.age,
         data.gender
     ]]

     hypertension_features = [[
         data.gender,
         data.age,
         data.currentSmoker,
         data.cigsPerDay,
         data.BPMeds,
         data.diabetes,
         data.totChol, data.sysBP, data.diaBP,
         data.BMI, data.heartRate, data.glucose
     ]]

     nfld_features = [[
         data.age,
         data.gender,
         data.BMI
     ]]
     

     pred01 = model01.predict(diabetes_features)
     pred02 = model02.predict(hypertension_features)
     pred03 = model03.predict(nfld_features)

     return {
         "Diabetes": pred01[0],
         "Hypertension": pred02[0],
         "NFLD": pred03[0]
     }

if __name__ == "__main__":
    import uvicorn


    uvicorn.run(app, host="0.0.0.0", port=8000)