import os
import json
import platform
import time
import random
import argparse
from tqdm import tqdm
import openai

# Determine platform and set paths
if os.name == 'nt':  # Windows
    ROOT = "Z:\\openai"
elif platform.system() == 'Darwin':  # macOS
    ROOT = "/Volumes/data-and-model/openai"
else:  # Linux or Azure Web App
    if "WEBSITE_INSTANCE_ID" in os.environ:  # Azure Web App detection
        ROOT = "/data-and-model/openai"
    else:
        ROOT = "/mnt/data-and-model/openai"

# Paths for the input and output files
DATA_PATH = os.path.join(
    ROOT,
    "train",
    "headlines",
    "News-Headlines-Dataset-For-Sarcasm-Detection-master",
    "Sarcasm_Headlines_Dataset.json",
)
HEADLINES_PATH = os.path.join(ROOT, "train", "headlines.jsonl")
HEADLINES_EMBEDDINGS_PATH_TEMPLATE = os.path.join(
    ROOT, "model", "headlines", "headlines_{epoch_time}.embeddings"
)
HEADLINES_EMBEDDINGS_PATH = os.path.join(ROOT, "model", "headlines", "headlines.embeddings")

# Load OpenAI API key
def load_api_key():
    apikey_path = os.path.join(os.path.dirname(__file__), "..", "tools", "apikey.txt")
    if not os.path.exists(apikey_path):
        raise FileNotFoundError(f"API key file not found at {apikey_path}")
    with open(apikey_path, "r") as file:
        return file.read().strip()

# Extract and sample "headline" field from JSONL input file
def extract_and_sample_headlines(input_path, output_path, sampling_ratio=0.01):
    """
    Extracts the "headline" field from the input JSONL file, samples a portion of records based on the sampling ratio,
    and saves the result to a JSONL file.

    :param input_path: Path to the input JSONL file.
    :param output_path: Path to the output JSONL file.
    :param sampling_ratio: Proportion of records to sample (between 0 and 1).
    """
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Ensure output directory exists

        # Read JSONL file line by line
        with open(input_path, "r", encoding="utf-8") as infile:
            data = [json.loads(line.strip()) for line in infile]

        # Randomly sample the data based on the sampling ratio
        sample_size = max(1, int(len(data) * sampling_ratio))  # Ensure at least one record is sampled
        sampled_data = random.sample(data, sample_size)

        # Write sampled data to JSONL
        with open(output_path, "w", encoding="utf-8") as outfile:
            for record in sampled_data:
                if "headline" in record:
                    json.dump({"headline": record["headline"]}, outfile, ensure_ascii=False)
                    outfile.write("\n")
        print(f"Sampled and extracted {sample_size} headlines to {output_path}")
    except Exception as e:
        print(f"Error during extraction and sampling: {e}")

# Generate embeddings using OpenAI API
def generate_embeddings(input_file, output_file, model="text-embedding-ada-002"):
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)  # Ensure output directory exists
        embeddings = []
        with open(input_file, "r", encoding="utf-8") as infile:
            for line in tqdm(infile, desc=f"Generating embeddings for {os.path.basename(input_file)}"):
                record = json.loads(line.strip())
                text = record.get("headline", "")
                if not text:
                    continue
                # Call OpenAI API to generate embeddings
                response = openai.Embedding.create(input=text, model=model)
                embedding = response["data"][0]["embedding"]
                embeddings.append({"record": record, "embedding": embedding})
        # Save embeddings to output file
        with open(output_file, "w", encoding="utf-8") as outfile:
            json.dump(embeddings, outfile)
        print(f"Embeddings saved to {output_file}")
    except Exception as e:
        print(f"Error during embedding generation: {e}")

# Main function
def main(sampling_ratio):
    """
    Main function to handle the process: sampling, extracting, and generating embeddings.

    :param sampling_ratio: Proportion of records to sample (between 0 and 1).
    """
    try:
        # Load OpenAI API key
        openai.api_key = load_api_key()

        # Step 1: Extract and sample "headline" field to JSONL
        extract_and_sample_headlines(DATA_PATH, HEADLINES_PATH, sampling_ratio)

        # Step 2: Generate embeddings and save them
        epoch_time = int(time.time())
        embeddings_output_path = HEADLINES_EMBEDDINGS_PATH_TEMPLATE.format(epoch_time=epoch_time)
        generate_embeddings(HEADLINES_PATH, embeddings_output_path)

        # Step 3: Copy latest embeddings to "headlines.embeddings"
        if os.path.exists(embeddings_output_path):
            os.makedirs(os.path.dirname(HEADLINES_EMBEDDINGS_PATH), exist_ok=True)
            with open(embeddings_output_path, "rb") as src, open(HEADLINES_EMBEDDINGS_PATH, "wb") as dest:
                dest.write(src.read())
            print(f"Updated latest embeddings at {HEADLINES_EMBEDDINGS_PATH}")

    except Exception as e:
        print(f"Error: {e}")

# Entry point
if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Process Sarcasm Headlines Dataset with sampling and OpenAI embeddings.")
    parser.add_argument(
        "--sampling_ratio", 
        type=float, 
        default=0.01, 
        help="Proportion of records to sample (between 0 and 1). Default is 0.01 (1%)."
    )
    args = parser.parse_args()

    # Call main with the provided sampling ratio
    main(sampling_ratio=args.sampling_ratio)
