# Import necessary modules from Flask
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from catboost import CatBoostClassifier
from sklearn.preprocessing import LabelEncoder

# Load the saved models
college_model = CatBoostClassifier()
college_model.load_model("Saved_Models/college_model.cbm")

branch_model = CatBoostClassifier()
branch_model.load_model("Saved_Models/branch_model.cbm")

# Create a Flask web application
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for the app
CORS(app)

# Create an empty list to store form data
form_data = []

# Function to preprocess the data
def preprocess_data(data):
    # Convert string values to float for the dictionary
    data['age'] = float(data['age'])
    data['sscMarks'] = float(data['sscMarks'])
    data['hscMarks'] = float(data['hscMarks'])
    data['mhtcetMarks'] = float(data['mhtcetMarks'])
    data['jeeMainsMarks'] = float(data['jeeMainsMarks'])

    return data

def make_predictions(data, top_n=3):
    print("Processed Data:", data)  # Add this line for debugging

    # Convert scalar values to lists
    data = {key: [value] for key, value in data.items()}

    # Convert list of dictionaries to DataFrame
    form_data_df = pd.DataFrame(data)

    # Encode categorical variables (Socioeconomic_Background)
    le = LabelEncoder()
    form_data_df['Socioeconomic_Background'] = le.fit_transform(form_data_df['socioeconomicBackground'])

    # Drop the original column after encoding
    form_data_df.drop(columns=['socioeconomicBackground'], inplace=True)

    # Convert the processed data into a DataFrame
    data_point = pd.DataFrame({
        'Age': form_data_df['age'],
        'Socioeconomic_Background': form_data_df['Socioeconomic_Background'],
        'SSC_Marks_Percentage': form_data_df['sscMarks'],
        'HSC_Marks_Percentage': form_data_df['hscMarks'],
        'MHTCET_Scores_Percentile': form_data_df['mhtcetMarks'],
        'JEE_Mains_Scores_Percentile': form_data_df['jeeMainsMarks']
    })

    # Make predictions
# new
    college_probs = college_model.predict_proba(data_point)
    branch_probs = branch_model.predict_proba(data_point)

    # Get the indices of the top N predictions
    top_n_college_indices = college_probs.argsort()[:, ::-1][:, :top_n]
    top_n_branch_indices = branch_probs.argsort()[:, ::-1][:, :top_n]

    # Get the top N predictions and their corresponding probabilities
    top_n_college_preds = college_model.classes_[top_n_college_indices]
    top_n_college_probs = np.array([college_probs[i, indices] for i, indices in enumerate(top_n_college_indices)])

    top_n_branch_preds = branch_model.classes_[top_n_branch_indices]
    top_n_branch_probs = np.array([branch_probs[i, indices] for i, indices in enumerate(top_n_branch_indices)])

    return top_n_college_preds.tolist(), top_n_branch_preds.tolist()

# Define a route to handle POST requests for submitting form data
@app.route('/submit-form', methods=['POST'])
def submit_form():
    # Get JSON data from the request
    data = request.json
    
    # Append the raw form data to the list
    form_data.append(data)
    
    # Return a JSON response indicating successful form data submission
    return jsonify({"message": "Form data received successfully"})

# For Debugging
# Define a route to handle GET requests for retrieving form data
@app.route('/get-form', methods=['GET'])
def get_form():
    # Return the stored form data as a JSON response
    return jsonify(form_data)

# Define a route to handle POST requests for making predictions
@app.route('/predict', methods=['POST'])
def predict():
    # Get JSON data from the request
    data = request.json
    
    # Preprocess the data
    processed_data = preprocess_data(data)
    
    # Make predictions
    college_preds, branch_preds = make_predictions(processed_data)
    
    # Return the predictions as a JSON response
    return jsonify({
        "collegePredictions": college_preds,
        "branchPredictions": branch_preds
    })

# Run the Flask app if the script is executed directly
if __name__ == '__main__':
    app.run(debug=True)