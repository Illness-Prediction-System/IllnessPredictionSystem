# Illness prediction system
## About this project
This is a Python project which uses machine learning to predict illnesses, based on data from [Disease-Symptom Dataset (Kaggle)](https://www.kaggle.com/datasets/dhivyeshrk/diseases-and-symptoms-dataset).

Started as a part of winter university practice.

## Running from source

### Important notice

Before you can run the main script, you need to have following files:
* `src/models/label_encoder.joblib`
* `src/models/logistic_regression.joblib`
* `src/models/scaler.joblib`

To interact with our database, one of the maintainers should start the EC2 server.

### Dependencies
This project requires:

* Faker (==40.1.2)
* imbalanced-learn (==0.14.1)
* joblib (==1.5.3)
* matplotlib (==3.10.8)
* numpy (==2.4.1)
* packaging (==26.0)
* pandas (==3.0.0)
* psycopg2-binary (==2.9.11)
* pyarrow (==23.0.0)
* PyQt6 (==6.10.2)
* python-dateutil (==2.9.0.post0)
* python-dotenv (==1.2.1)
* requests (==2.32.5)
* scikit-learn (==1.8.0)
* scipy (==1.17.0)
* six (==1.17.0)
* sklearn-compat (==0.1.5)
* threadpoolctl (==3.6.0)
* tzdata (==2025.3)
* uuid (==1.30)
* windrose (==1.9.2)
* xgboost (==3.1.3)

### Installation steps

Clone the repository:
```
git clone https://github.com/Illness-Prediction-System/IllnessPredictionSystem.git
cd IllnessPredictionSystem
```
Install required dependencies:
```
pip install -r requirements.txt
```
To make joblib files, run `src/pipeline.py`:
```
python -m src.pipeline
```
Once you have them, you can run the main program:
```
python -m main
```
## Assets

### Icons
All UI icons are from [Google Material Icons](https://github.com/google/material-design-icons) 
licensed under [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0.txt).

Copyright 2026 Google LLC.
