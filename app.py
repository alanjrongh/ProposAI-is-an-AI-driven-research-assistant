from flask import Flask, render_template, request
import joblib
import numpy as np
import docx
import pdfplumber
import plotly.graph_objects as go
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__, static_folder='static', template_folder='templates')

# Load traditional models
model = joblib.load(r"C:\Users\alanj\Downloads\Dr_ProposAI_Starter\backend\models\acceptance_model_enhanced.pkl")
tfidf = joblib.load(r"C:\Users\alanj\Downloads\Dr_ProposAI_Starter\backend\models\tfidf_vectorizer.pkl")
accepted_db = joblib.load(r"C:\Users\alanj\Downloads\Dr_ProposAI_Starter\backend\models\accepted_embeddings.pkl")

# -----------------------------------------------------
# Extract text from uploaded PDF or DOCX file
# -----------------------------------------------------
def extract_text(file_storage):
    filename = file_storage.filename.lower()
    if filename.endswith(".pdf"):
        try:
            file_storage.stream.seek(0)
            with pdfplumber.open(file_storage.stream) as pdf:
                text = "\n".join(page.extract_text() or '' for page in pdf.pages)
            return text
        except Exception as e:
            return f"Error reading PDF: {e}"
    elif filename.endswith(".docx"):
        try:
            file_storage.stream.seek(0)
            doc = docx.Document(file_storage.stream)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
        except Exception as e:
            return f"Error reading DOCX: {e}"
    return ""

# -----------------------------------------------------
# Main Route
# -----------------------------------------------------
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    result = None
    suggestions = ""
    similar = []
    title = ""
    abstract = ""
    speedometer_html = ""

    if 'file' in request.files:
        file = request.files['file']
        extracted = extract_text(file)
        if "Error" in extracted:
            return extracted
        abstract = extracted
        title = "Untitled Proposal"
    elif 'title' in request.form and 'abstract' in request.form:
        title = request.form['title']
        abstract = request.form['abstract']

    if abstract.strip():
        # --- Prediction ---
        combined_text = title + " " + abstract
        tfidf_vec = tfidf.transform([combined_text])
        prob = model.predict_proba(tfidf_vec)[0][1]
        label = "ACCEPTED" if prob > 0.5 else "REJECTED"
        result = {"label": label, "probability": f"{prob*100:.2f}%"}

        # --- Speedometer using Plotly ---
        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob * 100,
            title={'text': "Acceptance Probability"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "blue"},
                'steps': [
                    {'range': [0, 50], 'color': "red"},
                    {'range': [50, 75], 'color': "orange"},
                    {'range': [75, 100], 'color': "green"},
                ],
            }
        ))
        speedometer_html = gauge.to_html(full_html=False)

        # --- GPT-style Suggestions ---
        suggestions = (
            "• Clarify your methodology section.\n"
            "• Add stronger baseline comparisons.\n"
            "• Highlight the novelty more clearly in the abstract."
        )

        # --- Similar Accepted Proposals ---
        input_embed = similarity_model.encode(combined_text)
        accepted_titles = list(accepted_db.keys())
        accepted_embeds = np.array(list(accepted_db.values()))
        sims = cosine_similarity([input_embed], accepted_embeds)[0]
        top_indices = sims.argsort()[-3:][::-1]
        similar = [{"title": accepted_titles[i], "score": f"{sims[i]*100:.2f}%"} for i in top_indices]

    return render_template("index.html",
                           result=result,
                           speedometer=speedometer_html,
                           suggestions=suggestions,
                           similar=similar)

# -----------------------------------------------------
# Entry Point (Safe for Windows Multiprocessing)
# -----------------------------------------------------
if __name__ == "__main__":
    from sentence_transformers import SentenceTransformer

    app.config["specter"] = SentenceTransformer("allenai/specter")
    app.config["mpnet"] = SentenceTransformer("all-mpnet-base-v2")
    app.config["similarity_model"] = SentenceTransformer("all-MiniLM-L6-v2")

    app.run(debug=True)
