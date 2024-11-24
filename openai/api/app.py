from flask import Flask, request, jsonify
import os
import threading
import platform
import time
import json
import numpy as np
import openai

app = Flask(__name__)

# Determine the correct path for the model based on platform and environment
if os.name == 'nt':  # Windows
    MODEL_PATH = r"Z:\openai\model\headlines\headlines.embeddings"
elif platform.system() == 'Darwin':  # macOS
    MODEL_PATH = "/Volumes/data-and-model/openai/model/headlines/headlines.embeddings"
else:  # Linux or Azure Web App
    if "WEBSITE_INSTANCE_ID" in os.environ:  # Detecting Azure Web App
        MODEL_PATH = "/data-and-model/openai/model/headlines/headlines.embeddings"
    else:
        MODEL_PATH = "/mnt/data-and-model/openai/model/headlines/headlines.embeddings"

# Global variables for model, lock, and last modified time
model = None
model_lock = threading.Lock()
last_modified_time = None

# Load OpenAI API key
def load_api_key():
    apikey_path = os.path.join(os.path.dirname(__file__), "..", "tools", "apikey.txt")
    if not os.path.exists(apikey_path):
        raise FileNotFoundError(f"API key file not found at {apikey_path}")
    with open(apikey_path, "r") as file:
        return file.read().strip()

openai.api_key = load_api_key()

# Function to load or reload the model if updated
def load_model():
    global model, last_modified_time
    if os.path.exists(MODEL_PATH):
        with model_lock:
            current_modified_time = os.path.getmtime(MODEL_PATH)
            if model is None or current_modified_time != last_modified_time:
                with open(MODEL_PATH, "r", encoding="utf-8") as file:
                    model = json.load(file)  # Load embeddings from JSON file
                last_modified_time = current_modified_time
                print("Model loaded/reloaded successfully.")

# Generate reason for similarity using OpenAI GPT
def generate_similarity_reason(input_text, headline):
    prompt = f"""
    Analyze the following two texts and explain why they are similar:
    1. Input Text: {input_text}
    2. Suggested Headline: {headline}
    Provide a concise explanation of the similarity.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        reason = response["choices"][0]["message"]["content"].strip()
        return reason
    except Exception as e:
        print(f"Error in generating similarity reason: {e}")
        return "Unable to generate a similarity reason due to an error."

# Attempt to load the model initially
load_model()

@app.route('/api/detect', methods=['GET'])
def detect():
    # Load or reload the model if the file was updated
    load_model()

    # Check if the model is loaded
    if model is None:
        return jsonify({"error": "Model not found. Please ensure the embeddings file is available."}), 500

    # Get the text parameter from the request
    text = request.args.get("text", "").strip()
    if not text:
        return jsonify({"error": "The 'text' parameter is required."}), 400

    try:
        # Generate embedding for the input text
        response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
        input_embedding = np.array(response["data"][0]["embedding"])

        # Compare the input embedding to the model embeddings
        min_distance = float("inf")
        closest_headline = None

        for record in model:
            headline = record["record"]["headline"]
            embedding = np.array(record["embedding"])
            distance = np.linalg.norm(input_embedding - embedding)
            if distance < min_distance:
                min_distance = distance
                closest_headline = headline

        # Generate reason for similarity
        reason = generate_similarity_reason(text, closest_headline)

        # Return the closest headline, distance, and reason
        return jsonify({"headline": closest_headline, "distance": min_distance, "reason": reason})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)
