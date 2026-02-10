# Illness prediction system
## About this project
This is a work-in-progress Python project using machine learning to predict illnesses, based on data from [Disease-Symptom Dataset (Kaggle)](https://www.kaggle.com/datasets/dhivyeshrk/diseases-and-symptoms-dataset).

Started as a part of winter university practice.

## (WIP) Running from source

### IMPORTANT:
Running src/pipeline.py requires authorized access to the database.

### Dependencies
This project requires:

* Faker (==40.1.2)
* imbalanced-learn (==0.14.1)
* joblib (==1.5.3)
* numpy (==2.4.1)
* packaging (==26.0)
* pandas (==3.0.0)
* psycopg2-binary (==2.9.11)
* pyarrow (==23.0.0)
* PyQt6 (==6.10.2)
* python-dateutil (==2.9.0.post0)
* python-dotenv (==1.2.1)
* scikit-learn (==1.8.0)
* scipy (==1.17.0)
* six (==1.17.0)
* sklearn-compat (==0.1.5)
* threadpoolctl (==3.6.0)
* tzdata (==2025.3)
* uuid (==1.30)
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
Before you can run the main script, you need to have following files:
* `label_encoder.joblib`
* `logistic_regression.joblib`
* `scaler.joblib`
* `data/mappings/label_mapping_gender.json`
To make joblib files, run `src/pipeline.py` **(requires authorised connection to the database)**:
```
python -m src.pipeline
```
Once you have all the mentioned files, you can run the program:
```
python -m main
```
## Assets

### Icons
All UI icons are from [Google Material Icons](https://github.com/google/material-design-icons) 
licensed under [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0.txt).

Copyright 2023 Google LLC.