import os
import platform
import json
import time
import shutil
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

# Generate epoch time for filenames
epoch_time = int(time.time())

# File paths for epoch-named files
MODEL_PATH_EPOCH = os.path.join(ROOT, f"model/mbti_{epoch_time}.keras")
TOKENIZER_PATH_EPOCH = os.path.join(ROOT, f"model/tokenizer_{epoch_time}.json")
LABEL_ENCODER_PATH_EPOCH = os.path.join(ROOT, f"model/label_encoder_{epoch_time}.json")

# Default file paths (without epoch)
MODEL_PATH_DEFAULT = os.path.join(ROOT, "model/mbti.keras")
TOKENIZER_PATH_DEFAULT = os.path.join(ROOT, "model/tokenizer.json")
LABEL_ENCODER_PATH_DEFAULT = os.path.join(ROOT, "model/label_encoder.json")

# Load and preprocess data
def load_and_preprocess_data(data_path):
    # Load dataset from CSV
    df = pd.read_csv(data_path)

    # Preprocess posts
    def preprocess_posts(posts):
        return ' '.join(posts.split("|||"))  # Combine posts into one string

    df['posts'] = df['posts'].apply(preprocess_posts)

    # Randomly sample 30 records per label
    df = df.groupby('type').apply(lambda x: x.sample(n=30, random_state=42)).reset_index(drop=True)

    # Encode labels
    label_encoder = LabelEncoder()
    df['type_encoded'] = label_encoder.fit_transform(df['type'])

    # Tokenize text
    tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
    tokenizer.fit_on_texts(df['posts'])
    sequences = tokenizer.texts_to_sequences(df['posts'])
    padded_sequences = pad_sequences(sequences, padding='post', maxlen=500)

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        padded_sequences, df['type_encoded'], test_size=0.2, random_state=42
    )

    return X_train, X_test, y_train, y_test, tokenizer, label_encoder

# Build and train model
def build_and_train_model(X_train, y_train, X_test, y_test):
    # Build the model
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(input_dim=10000, output_dim=256, input_length=500),
        tf.keras.layers.SpatialDropout1D(0.3),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(128, return_sequences=True)),
        tf.keras.layers.GlobalMaxPooling1D(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.4),
        tf.keras.layers.Dense(len(set(y_train)), activation='softmax')
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    # Train the model: parameters can be adjusted for better accuracy
    # Please refer to the blog for more information
    model.fit(
        X_train, y_train,
        epochs=5,
        batch_size=16,
        validation_data=(X_test, y_test),
        verbose=1
    )

    return model

# Save model and assets
def save_model_and_assets(model, tokenizer, label_encoder, model_path_epoch, tokenizer_path_epoch, label_encoder_path_epoch):
    # Save the model
    os.makedirs(os.path.dirname(model_path_epoch), exist_ok=True)
    model.save(model_path_epoch)  # Save in `.keras` format

    # Save tokenizer
    with open(tokenizer_path_epoch, 'w') as file:
        file.write(tokenizer.to_json())

    # Save label encoder
    with open(label_encoder_path_epoch, 'w') as file:
        json.dump({
            "classes_": label_encoder.classes_.tolist()
        }, file)

# Copy files to default paths
def copy_to_default_paths(epoch_paths, default_paths):
    for epoch_path, default_path in zip(epoch_paths, default_paths):
        shutil.copy(epoch_path, default_path)
        print(f"Copied {epoch_path} to {default_path}")

# Main function
def main():
    # Path to CSV file
    DATA_PATH = os.path.join(ROOT, "train/mbti/MBTI-master/mbti_1.csv")  # Update this to the correct CSV file path

    # Load and preprocess data
    X_train, X_test, y_train, y_test, tokenizer, label_encoder = load_and_preprocess_data(DATA_PATH)

    # Build and train the model
    model = build_and_train_model(X_train, y_train, X_test, y_test)

    # Save model and assets
    save_model_and_assets(model, tokenizer, label_encoder, MODEL_PATH_EPOCH, TOKENIZER_PATH_EPOCH, LABEL_ENCODER_PATH_EPOCH)

    # Copy files to default paths
    epoch_paths = [MODEL_PATH_EPOCH, TOKENIZER_PATH_EPOCH, LABEL_ENCODER_PATH_EPOCH]
    default_paths = [MODEL_PATH_DEFAULT, TOKENIZER_PATH_DEFAULT, LABEL_ENCODER_PATH_DEFAULT]
    copy_to_default_paths(epoch_paths, default_paths)

    print("Training complete. Outputs:")
    print(f"Model saved as {MODEL_PATH_EPOCH}")
    print(f"Tokenizer saved as {TOKENIZER_PATH_EPOCH}")
    print(f"Label encoder saved as {LABEL_ENCODER_PATH_EPOCH}")
    print("Default paths updated.")

if __name__ == "__main__":
    main()