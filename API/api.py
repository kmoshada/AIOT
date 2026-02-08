from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import contextlib

class Diabetes(BaseModel):
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
    BMI: float


app = FastAPI()

@app.get("/")
def read():
    return {"Hello": "World"}




if __name__ == "__main__":
    import uvicorn


    uvicorn.run(app, host="0.0.0.0", port=8000)