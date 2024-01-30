# Import necessary modules from Flask
from flask import Flask, request, jsonify
from flask_cors import CORS

# Create a Flask web application
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for the app
CORS(app)

# Create an empty list to store form data
form_data = []

# Define a route to handle POST requests for submitting form data
@app.route('/form-data', methods=['POST'])
def handle_form_data():
    # Get JSON data from the request
    data = request.json
    # Extract specific keys from the data and append to the form_data list
    form_data.append({key: data.get(key) for key in ['age', 'socioeconomicBackground', 'sscMarks', 'hscMarks', 'mhtcetMarks', 'jeeMainsMarks']})
    # Return a JSON response indicating successful form data submission
    return jsonify({"message": "Form data received successfully"})

# Define a route to handle GET requests for retrieving form data
@app.route('/get-form-data', methods=['GET'])
def get_form_data():
    # Return the stored form data as a JSON response
    return jsonify(form_data)

# Run the Flask app if the script is executed directly
if __name__ == '__main__':
    app.run(debug=True)