from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

print(f"Downloading model {MODEL_NAME}...")

model = SentenceTransformer(MODEL_NAME)  # Automatically downloads to cache

print("Model downloaded and cached successfully!")
