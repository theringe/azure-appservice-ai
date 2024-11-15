from flask import Flask, request, jsonify
import joblib
import os
import threading
import platform

app = Flask(__name__)

# Determine the correct path for the model based on platform and environment
if os.name == 'nt':  # Windows
    MODEL_PATH = r"Z:\scikit-learn\model\heart_disease_model.joblib"
elif platform.system() == 'Darwin':  # macOS
    MODEL_PATH = "/Volumes/data-and-model/scikit-learn/model/heart_disease_model.joblib"
else:  # Linux or Azure
    if "WEBSITE_INSTANCE_ID" in os.environ:  # Detecting Azure
        MODEL_PATH = "/data-and-model/scikit-learn/model/heart_disease_model.joblib"
    else:
        MODEL_PATH = "/mnt/data-and-model/scikit-learn/model/heart_disease_model.joblib"

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
    app.run(debug=True, host="0.0.0.0", port=8000)
