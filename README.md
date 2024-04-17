# About: 

This project serves as the backend for the student prediction web application, providing the necessary infrastructure and functionality to support the frontend interface. Built with Flask, a lightweight and flexible Python web framework, the backend encompasses several key components essential for the application's operation.

At its core, the backend handles data processing tasks such as data generation, cleaning, and preprocessing. It incorporates machine learning algorithms for model training and evaluation, utilizing historical student data to build predictive models capable of estimating the likelihood of admission to preferred branches or colleges.

Additionally, the backend facilitates communication between the frontend interface and the machine learning model, enabling seamless integration of prediction functionality into the web application. Through RESTful API endpoints, the frontend can send user input data to the backend for prediction, receiving the results to display to the user in real-time.

With robust error handling and logging mechanisms, the backend ensures reliability and stability, providing a dependable foundation for the overall application. Scalable and extensible, it is designed to accommodate future enhancements and optimizations, ensuring continued effectiveness and relevance in the dynamic landscape of college admissions.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/KarthikShetty27/project-backend.git
   ```

2. **Navigate to the project directory:**
   ```bash
   cd project-backend
   ```

3. **Set up a Python virtual environment:**
   ```bash
   python -m venv venv
   ```

4. **Activate the virtual environment:**
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On macOS / Linux:
     ```bash
     source venv/bin/activate
     ```

5. **Install dependencies using pip:**
   ```bash
   pip install -r requirements.txt
   ```

## How to Run the Project

1. **Start the Flask server using the provided script:**
   ```
   .\Scripts\run_flask.ps1
   ```

2. The Flask server will be running at `http://localhost:5000`.



## How to End the Project

1. **Stop/End the Flask server using the provided script:**
   ```
   .\Scripts\end_venv.ps1
   ```