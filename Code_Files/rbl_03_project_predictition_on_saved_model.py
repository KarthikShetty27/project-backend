# -*- coding: utf-8 -*-
"""RBL_03_Project_Predictition_on_saved_model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dP1CZGHJNsfvwS4RTcNalB11e5gz8PUf
"""

# Import necessary libraries
import pandas as pd
from catboost import CatBoostClassifier
from sklearn.preprocessing import LabelEncoder

# Load the saved models
college_model = CatBoostClassifier()
college_model.load_model("../Saved_Models/college_model.cbm")

branch_model = CatBoostClassifier()
branch_model.load_model("../Saved_Models/branch_model.cbm")

# Define the test data in the format provided
form_data = [{"age":"20","hscMarks":"88.64","jeeMainsMarks":"93.26","mhtcetMarks":"90.85","socioeconomicBackground":"Open","sscMarks":"85.65"}]

# Convert list of dictionaries to DataFrame
form_data_df = pd.DataFrame(form_data)

# Encode categorical variables (Socioeconomic_Background)
le = LabelEncoder()
form_data_df['Socioeconomic_Background'] = le.fit_transform(form_data_df['socioeconomicBackground'])

# Drop the original column after encoding
form_data_df.drop(columns=['socioeconomicBackground'], inplace=True)

form_data_df

# Function to preprocess the data
def preprocess_data(data):
    # Convert string values to float where necessary
    for entry in data:
        entry['age'] = float(entry['age'])
        entry['hscMarks'] = float(entry['hscMarks'])
        entry['jeeMainsMarks'] = float(entry['jeeMainsMarks'])
        entry['mhtcetMarks'] = float(entry['mhtcetMarks'])
        entry['sscMarks'] = float(entry['sscMarks'])
    return data

# Preprocess the test data
processed_data = preprocess_data(form_data)

processed_data

# Convert the processed data into a DataFrame
data_point = pd.DataFrame({
    'Age': [float(processed_data[0]["age"])],
    'Socioeconomic_Background': [form_data_df['Socioeconomic_Background'][0]],
    'SSC_Marks_Percentage': [float(processed_data[0]["sscMarks"])],
    'HSC_Marks_Percentage': [float(processed_data[0]["hscMarks"])],
    'MHTCET_Scores_Percentile': [float(processed_data[0]["mhtcetMarks"])],
    'JEE_Mains_Scores_Percentile': [float(processed_data[0]["jeeMainsMarks"])]
})

# Function to make predictions using the models
def make_predictions(data):
    college_predictions = college_model.predict(data)
    branch_predictions = branch_model.predict(data)
    return college_predictions, branch_predictions

# Make predictions
college_preds, branch_preds = make_predictions(data_point)

# Print the predictions
print("College Predictions:", college_preds)
print("Branch Predictions:", branch_preds)