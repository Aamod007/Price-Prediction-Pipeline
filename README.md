# House Price Predictor - End-to-End MLOps System

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://python.org)
[![ZenML](https://img.shields.io/badge/MLOps-ZenML-purple.svg)](https://zenml.io)
[![MLflow](https://img.shields.io/badge/Tracking-MLflow-blue.svg)](https://mlflow.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

An end-to-end, production-grade Machine Learning pipeline for predicting house prices. This project utilizes modern MLOps tools to create a robust, reproducible, and trackable machine learning workflow with Continuous Deployment.

## Table of Contents
- [Overview](#overview)
- [Architecture & Dashboards](#architecture--dashboards)
- [Pipeline Steps](#pipeline-steps)
- [Installation](#installation)
- [Usage](#usage)

## Overview
This repository contains a full ML pipeline designed to ingest raw housing data, clean it, train a Gradient Boosting regression model, and evaluate its performance. It also includes a continuous deployment pipeline that deploys the trained model as a prediction service using MLflow. Instead of standalone Jupyter notebooks, this project uses **ZenML** for orchestration and **MLflow** for experiment tracking and model serving to ensure every step is modular, cached, and production-ready.

## Dataset & Performance Metrics
- **Dataset**: Ames Housing Dataset (2,930 entries, 82 features)
- **Key Metrics Achieved**:
  - **R-Squared (R²)**: 0.920
  - **Root Mean Squared Error (RMSE)**: 0.106
  - **Mean Absolute Error (MAE)**: 0.073
  - **Mean Squared Error (MSE)**: 0.011

## Architecture & Dashboards

### ZenML Pipeline DAG
ZenML orchestrates the workflow. Below is the directed acyclic graph (DAG) of the ML pipeline:

![ZenML Dashboard](assets/Screenshot%202026-06-10%20204203.png)

### MLflow Experiment Tracking
MLflow automatically logs all models, metrics (MSE, RMSE, MAE, R-Squared), and schema artifacts. You can track your experiments and view registered models:

**Experiments View:**
![MLflow Experiments](assets/Screenshot%202026-06-10%20204218.png)

**Model Registry & Deployments:**
![MLflow Models](assets/Screenshot%202026-06-10%20204254.png)

### MLflow Metric Charts
You can also visualize the logged metrics as charts over multiple runs to compare model performance:

![MLflow Metrics](assets/Screenshot%202026-06-10%20204353.png)

## Pipeline Steps

### 1. Training Pipeline (`pipelines/training_pipeline.py`)
1. **Data Ingestion** (`data_ingestion_step`): Loads raw data from a zip archive.
2. **Handle Missing Values** (`handle_missing_values_step`): Imputes missing data using statistical methods (e.g., mean imputation).
3. **Feature Engineering** (`feature_engineering_step`): Applies log transformations to skewed features.
4. **Outlier Detection** (`outlier_detection_step`): Removes anomalies using Z-score methods.
5. **Data Splitting** (`data_splitter_step`): Splits the dataset into training and testing sets.
6. **Model Building** (`model_building_step`): Trains a Gradient Boosting Regressor model.
7. **Model Evaluation** (`model_evaluator_step`): Computes MSE, RMSE, MAE, and R-Squared metrics on the test set.

### 2. Continuous Deployment Pipeline (`pipelines/deployment_pipeline.py`)
1. **Training Pipeline Integration**: Executes the training pipeline to produce a model.
2. **Model Deployment** (`mlflow_model_deployer_step`): Deploys the trained Gradient Boosting model as a local prediction service daemon using MLflow.
3. **Inference Pipeline**: Loads batch data and hits the local prediction service endpoint to generate predictions.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Aamod007/Price-Prediction-Pipeline.git
cd Price-Prediction-Pipeline
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: .\venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
zenml integration install mlflow -y
```

## Usage

### 1. Initialize ZenML and MLflow Stack
Set up the tracking tools and deployer locally:
```bash
zenml experiment-tracker register mlflow_tracker --flavor=mlflow
zenml model-deployer register mlflow_deployer --flavor=mlflow
zenml stack register mlflow_stack -a default -o default -e mlflow_tracker -d mlflow_deployer --set
```

### 2. Run the Pipelines
To run just the training pipeline:
```bash
python run_pipeline.py
```

To run the continuous deployment pipeline and deploy the model:
```bash
python run_deployment.py
```

To test the live prediction endpoint:
```bash
python sample_predict.py
```

### 3. View the Dashboards
To view your pipeline execution graph in ZenML:
```bash
zenml login --local --blocking
# Open http://127.0.0.1:8237 in your browser
```

To view your tracked experiments and metrics in MLflow:
```bash
# Set file store flag to allow local tracking
export MLFLOW_ALLOW_FILE_STORE=true
mlflow ui --backend-store-uri 'file:./mlruns'
```

---
*Built by Aamod Kumar with ZenML & MLflow.*
