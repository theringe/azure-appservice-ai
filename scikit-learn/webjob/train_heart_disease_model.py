import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
import time
import shutil

# Step 1: Define root folder based on the OS and environment
if os.name == 'nt':  # Windows
    ROOT = "Z:\\scikit-learn"
else:  # Linux or other Unix-like OS
    # Check if running on Azure Web App by looking for the 'WEBSITE_INSTANCE_ID' environment variable
    if "WEBSITE_INSTANCE_ID" in os.environ:
        ROOT = "/data-and-model/scikit-learn"
    else:
        ROOT = "/mnt/data-and-model/scikit-learn"

DATA_PATH = os.path.join(ROOT, "train", "heart_disease", "processed.cleveland.data")  # Adjust filename as needed
MODEL_DIR = os.path.join(ROOT, "model")
FINAL_MODEL_PATH = os.path.join(MODEL_DIR, "heart_disease_model.joblib")

# Step 2: Load the dataset
column_names = [
    "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
    "thalach", "exang", "oldpeak", "slope", "ca", "thal", "target"
]
df = pd.read_csv(DATA_PATH, names=column_names, na_values="?")

# Step 3: Preprocess the data
# Drop rows with missing values
df = df.dropna()

# Separate features and target
X = df.drop("target", axis=1)
y = df["target"]

# Binary classification (1 if heart disease, 0 if no heart disease)
y = y.apply(lambda x: 1 if x > 0 else 0)

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Train a model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Step 5: Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Step 6: Save the trained model with timestamp and replace the final model file
os.makedirs(MODEL_DIR, exist_ok=True)

# Generate a unique model filename with epoch time
epoch_time = int(time.time())
timestamped_model_path = os.path.join(MODEL_DIR, f"heart_disease_model_{epoch_time}.joblib")
joblib.dump(model, timestamped_model_path)
print(f"Model saved as {timestamped_model_path}")

# Replace (or create) the final model file with the latest model
shutil.copy(timestamped_model_path, FINAL_MODEL_PATH)
print(f"Final model file updated to {FINAL_MODEL_PATH}")
