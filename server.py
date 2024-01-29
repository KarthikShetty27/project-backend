# server.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/form-data', methods=['GET', 'POST'])
def handle_form_data():
    if request.method == 'POST':
        data = request.json

        age = data.get('age')
        socioeconomic_background = data.get('socioeconomicBackground')
        ssc_marks = data.get('sscMarks')
        hsc_marks = data.get('hscMarks')
        mhtcet_marks = data.get('mhtcetMarks')
        jee_mains_marks = data.get('jeeMainsMarks')

        # Render the HTML template with the printed data
        return render_template('form-data.html', 
                               age=age,
                               socioeconomic_background=socioeconomic_background,
                               ssc_marks=ssc_marks,
                               hsc_marks=hsc_marks,
                               mhtcet_marks=mhtcet_marks,
                               jee_mains_marks=jee_mains_marks)
    elif request.method == 'GET':
        # Handle GET request logic here, if needed
        return render_template('form-data.html')  # or any other response
    
    return render_template('form-data.html')

    # Return a 405 error if the request method is not supported
    return jsonify({"error": "Method Not Allowed"}), 405

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
