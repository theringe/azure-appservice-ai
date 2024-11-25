import json
import os
import platform
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

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

# File paths
DATA_PATH = os.path.join(ROOT, "train/mbti/MBTI-master/mbti_1.csv")
MODEL_PATH = os.path.join(ROOT, "model/mbti.keras")
TOKENIZER_PATH = os.path.join(ROOT, "model/tokenizer.json")
LABEL_ENCODER_PATH = os.path.join(ROOT, "model/label_encoder.json")

# Load and preprocess data
def load_and_preprocess_data(data_path):
    # Load dataset
    df = pd.read_csv(data_path)

    # Preprocess posts
    def preprocess_posts(posts):
        return ' '.join(posts.split("|||"))  # Combine posts into one string

    df['posts'] = df['posts'].apply(preprocess_posts)

    # Encode labels
    label_encoder = LabelEncoder()
    df['type_encoded'] = label_encoder.fit_transform(df['type'])

    # Tokenize text
    tokenizer = Tokenizer(num_words=20000, oov_token="<OOV>")
    tokenizer.fit_on_texts(df['posts'])
    sequences = tokenizer.texts_to_sequences(df['posts'])
    padded_sequences = pad_sequences(sequences, padding='post', maxlen=1000)

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        padded_sequences, df['type_encoded'], test_size=0.2, random_state=42
    )

    return X_train, X_test, y_train, y_test, tokenizer, label_encoder

# Build and train model
def build_and_train_model(X_train, y_train, X_test, y_test):
    # Build the model
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(20000, 128, input_length=1000),
        tf.keras.layers.GlobalAveragePooling1D(),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(len(set(y_train)), activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    # Train the model
    model.fit(
        X_train, y_train,
        epochs=5,
        batch_size=32,
        validation_data=(X_test, y_test)
    )

    return model

# Save model and assets
def save_model_and_assets(model, tokenizer, label_encoder, model_path, tokenizer_path, label_encoder_path):
    # Save the model
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    model.save(model_path)  # Save in `.keras` format

    # Save tokenizer
    with open(tokenizer_path, 'w') as file:
        file.write(tokenizer.to_json())

    # Save label encoder
    with open(label_encoder_path, 'w') as file:
        json.dump({
            "classes_": label_encoder.classes_.tolist()
        }, file)

# Main function
def main():
    # Load and preprocess data
    X_train, X_test, y_train, y_test, tokenizer, label_encoder = load_and_preprocess_data(DATA_PATH)

    # Build and train the model
    model = build_and_train_model(X_train, y_train, X_test, y_test)

    # Save model and assets
    save_model_and_assets(model, tokenizer, label_encoder, MODEL_PATH, TOKENIZER_PATH, LABEL_ENCODER_PATH)

    print("Training complete. Model and assets saved successfully.")

if __name__ == "__main__":
    main()
