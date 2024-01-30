# server.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

form_data = []

@app.route('/form-data', methods=['POST'])
def handle_form_data():
    global form_data
    data = request.json

    age = data.get('age')
    socioeconomic_background = data.get('socioeconomicBackground')
    ssc_marks = data.get('sscMarks')
    hsc_marks = data.get('hscMarks')
    mhtcet_marks = data.get('mhtcetMarks')
    jee_mains_marks = data.get('jeeMainsMarks')

    # Append the form data to the array
    form_data.append({
        "age": age,
        "socioeconomic_background": socioeconomic_background,
        "ssc_marks": ssc_marks,
        "hsc_marks": hsc_marks,
        "mhtcet_marks": mhtcet_marks,
        "jee_mains_marks": jee_mains_marks
    })

    return jsonify({"message": "Form data received successfully"})

@app.route('/get-form-data', methods=['GET'])
def get_form_data():
    global form_data
    return jsonify(form_data)

@app.route('/display-form-data')
def display_form_data():
    return render_template('form-data.html', form_data=form_data)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
