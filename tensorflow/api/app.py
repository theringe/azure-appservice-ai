from flask import Flask, request, jsonify
import os
import platform
import json
import tensorflow as tf
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Determine platform and set paths
if os.name == 'nt':  # Windows
    ROOT = "Z:\\tensorflow"
elif platform.system() == 'Darwin':  # macOS
    ROOT = "/Volumes/data-and-model/tensorflow"
else:  # Linux or Azure Web App
    if "WEBSITE_INSTANCE_ID" in os.environ:  # Azure Web App detection
        ROOT = "/data-and-model/tensorflow"
    else:
        ROOT = "/mnt/data-and-model/tensorflow"

# Define paths
MODEL_PATH = os.path.join(ROOT, "model/mbti.keras")
TOKENIZER_PATH = os.path.join(ROOT, "model/tokenizer.json")
LABEL_ENCODER_PATH = os.path.join(ROOT, "model/label_encoder.json")

# Load model
model = tf.keras.models.load_model(MODEL_PATH)

# Load tokenizer
with open(TOKENIZER_PATH, 'r') as file:
    tokenizer = tokenizer_from_json(file.read())

# Load label encoder
with open(LABEL_ENCODER_PATH, 'r') as file:
    label_encoder_data = json.load(file)
    label_classes = label_encoder_data["classes_"]

# Flask app
app = Flask(__name__)

@app.route('/api/detect', methods=['GET'])
def detect():
    input_text = request.json.get("post", "")
    if not input_text:
        return jsonify({"error": "The 'post' field is required."}), 400

    # Preprocess input
    sequences = tokenizer.texts_to_sequences([input_text])
    padded = pad_sequences(sequences, maxlen=1000, padding='post')

    # Predict
    prediction = model.predict(padded)
    # print(prediction)  # Log predicted probabilities
    predicted_class = label_classes[prediction.argmax()]

    return jsonify({"MBTI": predicted_class})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
