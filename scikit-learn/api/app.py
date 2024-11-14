from flask import Flask, request, jsonify
import joblib
import os
import threading

app = Flask(__name__)

# Define the path to the model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "heart_disease_model.joblib")

# Initialize model, lock, and last modified time
model = None
model_lock = threading.Lock()
last_modified_time = None

def load_model():
    global model, last_modified_time
    if os.path.exists(MODEL_PATH):
        with model_lock:
            # Check if the model file has been modified since last load
            current_modified_time = os.path.getmtime(MODEL_PATH)
            if model is None or current_modified_time != last_modified_time:
                model = joblib.load(MODEL_PATH)
                last_modified_time = current_modified_time
                print("Model loaded/reloaded successfully.")

# Attempt to load the model initially
load_model()

@app.route('/api/detect', methods=['GET'])
def detect():
    # Load or reload the model if the file was updated
    load_model()
    
    # Check if the model is loaded
    if model is None:
        return jsonify({"error": "Model not found. Please build the model first."}), 500

    # Get the JSON data
    data = request.get_json()

    # Check if 'info' parameter is present in the data
    if not data or 'info' not in data:
        return jsonify({"error": "Missing 'info' parameter"}), 400
    
    info = data['info']

    try:
        # Assuming info is a list or numpy array of features for prediction
        prediction = model.predict([info])[0]  # Adjust this line based on your model's expected input format
        result = "Heart Disease" if prediction == 1 else "No Heart Disease"
        
        # Return the result as JSON
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
