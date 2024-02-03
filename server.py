# Import necessary modules from Flask
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
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
    if isinstance(data, list):
        # Convert string values to float where necessary for each entry in the list
        for entry in data:
            entry['age'] = float(entry['age'])
            entry['hscMarks'] = float(entry['hscMarks'])
            entry['jeeMainsMarks'] = float(entry['jeeMainsMarks'])
            entry['mhtcetMarks'] = float(entry['mhtcetMarks'])
            entry['sscMarks'] = float(entry['sscMarks'])
    else:
        # Convert string values to float for a single dictionary
        data['age'] = float(data['age'])
        data['hscMarks'] = float(data['hscMarks'])
        data['jeeMainsMarks'] = float(data['jeeMainsMarks'])
        data['mhtcetMarks'] = float(data['mhtcetMarks'])
        data['sscMarks'] = float(data['sscMarks'])
    return data

# Function to make predictions using the models
def make_predictions(data):
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
    college_preds = college_model.predict(data_point)
    branch_preds = branch_model.predict(data_point)
    
    return college_preds, branch_preds

# Define a route to handle POST requests for submitting form data
@app.route('/submit-form', methods=['POST'])
def submit_form():
    # Get JSON data from the request
    data = request.json
    
    # Append the raw form data to the list
    form_data.append(data)
    
    # Return a JSON response indicating successful form data submission
    return jsonify({"message": "Form data received successfully"})

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
    processed_data = preprocess_data([data])
    
    # Make predictions
    college_preds, branch_preds = make_predictions(processed_data)
    
    # Return the predictions as a JSON response
    return jsonify({
        "collegePredictions": college_preds.tolist(),
        "branchPredictions": branch_preds.tolist()
    })

# Run the Flask app if the script is executed directly
if __name__ == '__main__':
    app.run(debug=True)