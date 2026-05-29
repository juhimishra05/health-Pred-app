# Health Prediction System

## Overview

Health Prediction System is a Flask-based web application that allows users to manage patient health records and predict possible health risks using a Machine Learning model.

## Features

* Add Patient Records
* View Patient Records
* Update Patient Records
* Delete Patient Records
* Health Risk Prediction using Decision Tree Machine Learning Model
* SQLite Database Storage
* Bootstrap Responsive UI

## Technologies Used

* Python
* Flask
* SQLite
* Bootstrap 5
* Scikit-Learn
* Joblib

## Machine Learning

A Decision Tree Classifier is trained using healthcare sample data containing:

* Glucose
* Haemoglobin
* Cholesterol

The model predicts possible health risks and stores the prediction in the Remarks field.

## Installation

```bash
pip install -r requirements.txt
python train_model.py
python app.py
```

## Author

Juhi Mishra
