# 🏥 AIOT — AI-Powered Health Risk Prediction API

> A machine learning inference API that predicts **Diabetes**, **Hypertension**, and **MASLD (Metabolic dysfunction–Associated Steatotic Liver Disease)** using a single set of patient vitals.

---

## 📌 Overview

**AIOT** is an AI-based health screening system built with FastAPI and scikit-learn. It provides a single REST endpoint that runs three separate machine learning models at once, delivering risk predictions for three major chronic conditions in one request.

This project covers the complete machine learning workflow, including data collection and cleaning, model training, and deployment through a production-ready API.

---

## 🔬 Predicted Conditions

| Condition | Model File | Key Input Features |
|---|---|---|
| **Diabetes** | `diabetes_model.joblib` | Age, Gender, Glucose Level |
| **Hypertension** | `hypertension_model.joblib` | Gender, Age, Smoking, BP Meds, Cholesterol, BP, BMI, Heart Rate, Glucose |
| **NAFLD** | `nafld_model.joblib` | Age, Gender, BMI |

> **Note:** The Hypertension model uses the Diabetes prediction as one of its input features, creating a chained inference pipeline.

---

## 📂 Project Structure

```
AIOT/
├── API/
│   ├── api.py                      # FastAPI application — main entry point
│   └── Modules/
│       ├── diabetes_model.joblib   # Trained Diabetes classifier (~262 KB)
│       ├── hypertension_model.joblib  # Trained Hypertension classifier (~4.5 MB)
│       └── nafld_model.joblib      # Trained NAFLD classifier (~2 MB)
│
├── Code/
│   ├── cleaning.ipynb              # Data cleaning & preprocessing notebook
│   └── Traning.ipynb               # Model training & evaluation notebook
│
├── Raw Datasets/
│   ├── diabetes_dataset.csv        # Raw diabetes diagnosis data (Kaggle)
│   ├── Hypertension-risk-model-main.csv  # Raw hypertension risk data (Kaggle)
│   └── nafld1.csv                  # Raw NAFLD study data (Kaggle)
│
├── Clean Datasets/                 # Processed datasets ready for training
├── DATA DETILE.txt                 # Dataset sources & feature descriptions
└── README.md
```

---

## 📊 Datasets

All datasets are sourced from [Kaggle](https://www.kaggle.com).

### 1. Diabetes Diagnosis Dataset
🔗 [abhayayare/diabetes-diagnosis-dataset](https://www.kaggle.com/datasets/abhayayare/diabetes-diagnosis-dataset/data)

| Feature | Description |
|---|---|
| `Age` | Patient age |
| `Gender` | Patient gender (encoded) |
| `Blood_Glucose_Level` | Measured blood glucose level |
| `Diagnosis` | **Target** — `Positive` / `Negative` |

---

### 2. Hypertension Risk Model
🔗 [khan1803115/hypertension-risk-model-main](https://www.kaggle.com/datasets/khan1803115/hypertension-risk-model-main/data)

| Feature | Description |
|---|---|
| `male` | Gender (binary) |
| `age` | Age of the individual |
| `currentSmoker` | Smoking status |
| `cigsPerDay` | Cigarettes smoked per day |
| `BPMeds` | Blood pressure medication usage |
| `diabetes` | Diabetes status (fed from Model 1 output) |
| `totChol` | Total cholesterol level |
| `sysBP` | Systolic blood pressure |
| `diaBP` | Diastolic blood pressure |
| `BMI` | Body mass index |
| `heartRate` | Heart rate |
| `glucose` | Glucose level |
| `Risk` | **Target** — hypertension risk status |

---

### 3. Non-Alcoholic Fatty Liver Disease (NAFLD)
🔗 [utkarshx27/non-alcohol-fatty-liver-disease](https://www.kaggle.com/datasets/utkarshx27/non-alcohol-fatty-liver-disease?select=nafld1.csv)

| Feature | Description |
|---|---|
| `age` | Age at study entry |
| `male` | Gender (0=female, 1=male) |
| `bmi` | Body mass index |
| `status` | **Target** — `0`=alive at follow-up, `1`=dead |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd AIOT

# Install dependencies
pip install fastapi uvicorn scikit-learn joblib pydantic
```

### Running the API

```bash
cd API
python api.py
```

The server will start at `http://0.0.0.0:8000`.

Alternatively, use `uvicorn` directly:

```bash
cd API
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

---

## 📡 API Reference

### `GET /`
Health check endpoint.

**Response:**
```json
{ "Hello": "World" }
```

---

### `POST /predict`
Run all three health risk predictions from a single patient profile.

**Request Body:**

```json
{
  "gender": 1,
  "age": 45,
  "currentSmoker": 0,
  "cigsPerDay": 0.0,
  "BPMeds": 0,
  "totChol": 230.5,
  "sysBP": 125.0,
  "diaBP": 80.0,
  "BMI": 27.3,
  "heartRate": 72.0,
  "glucose": 95.0
}
```

| Field | Type | Description |
|---|---|---|
| `gender` | `int` | `0` = Female, `1` = Male |
| `age` | `int` | Patient age in years |
| `currentSmoker` | `int` | `0` = No, `1` = Yes |
| `cigsPerDay` | `float` | Average cigarettes per day |
| `BPMeds` | `int` | `0` = No medication, `1` = On medication |
| `totChol` | `float` | Total cholesterol (mg/dL) |
| `sysBP` | `float` | Systolic blood pressure (mmHg) |
| `diaBP` | `float` | Diastolic blood pressure (mmHg) |
| `BMI` | `float` | Body mass index (kg/m²) |
| `heartRate` | `float` | Resting heart rate (bpm) |
| `glucose` | `float` | Blood glucose level (mg/dL) |

**Response:**

```json
{
  "Diabetes": 0,
  "Hypertension": 1,
  "NFLD": 0
}
```

| Key | Value | Meaning |
|---|---|---|
| `Diabetes` | `0` / `1` | `1` = Positive for Diabetes |
| `Hypertension` | `0` / `1` | `1` = High Hypertension Risk |
| `NFLD` | `0` / `1` | `1` = NAFLD Risk (mortality at follow-up) |

---

## 🧠 ML Pipeline

The full training pipeline is documented in the Jupyter notebooks inside `/Code`:

1. **`cleaning.ipynb`** — Raw dataset loading, handling missing values, feature encoding, and merging steps.
2. **`Traning.ipynb`** — Model selection, training, evaluation metrics, and serializing the final models with `joblib`.

The models are persisted as `.joblib` files inside `API/Modules/` and loaded at server startup.

---

## 🔗 Interactive Docs

Once the server is running, FastAPI provides auto-generated interactive documentation:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## ⚠️ Disclaimer

This project is intended for **educational and research purposes only**. The predictions made by these models are **not a substitute for professional medical diagnosis**. Always consult a qualified healthcare professional for medical decisions.

---

## 📄 License

This project is open source. See your preferred license file for details.
