import os
import json
import torch
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sentence_transformers import SentenceTransformer
import lightgbm as lgb
import joblib
from imblearn.over_sampling import SMOTE

# Check GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🔍 Using device: {device}")

# Load dataset (adjusted path for backend folder)
with open("../data/final_balanced_dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Prepare data
df = pd.DataFrame(data)
df["full_text"] = df["title"].fillna("") + " " + df["text"].fillna("")
labels = df["label"].values

# Generate embeddings
print("🔄 Generating SPECTER embeddings...")
specter = SentenceTransformer("allenai/specter", device=device)
specter_embeddings = specter.encode(df["full_text"].tolist(), show_progress_bar=True)

print("🔄 Generating MPNet embeddings...")
mpnet = SentenceTransformer("all-mpnet-base-v2", device=device)
mpnet_embeddings = mpnet.encode(df["full_text"].tolist(), show_progress_bar=True)

# TF-IDF
print("🔄 Generating TF-IDF features...")
tfidf = TfidfVectorizer(max_features=1000)
tfidf_matrix = tfidf.fit_transform(df["full_text"]).toarray()

# Combine all features
X = np.hstack([specter_embeddings, mpnet_embeddings, tfidf_matrix])
y = labels

# Balance the dataset using SMOTE
print("⚖️  Balancing classes with SMOTE...")
X, y = SMOTE(random_state=42).fit_resample(X, y)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Train model
print("🚀 Training LightGBM classifier...")
model = lgb.LGBMClassifier(n_estimators=500, learning_rate=0.05, max_depth=8, random_state=42)
model.fit(X_train, y_train)

# Evaluate
print("📊 Model Evaluation:")
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred, digits=4))

# Save the model and vectorizer
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/acceptance_model_enhanced.pkl")
joblib.dump(tfidf, "models/tfidf_vectorizer.pkl")

print("✅ Model and vectorizer saved to 'models/' folder.")
