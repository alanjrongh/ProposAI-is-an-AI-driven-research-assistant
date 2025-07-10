ProposAI – AI-Powered Research Proposal Assistant
ProposAI is an AI-driven assistant designed to enhance the research proposal process. By predicting the likelihood of acceptance, generating reviewer-style feedback, and suggesting similar accepted papers from a global dataset, ProposAI helps researchers improve the quality and impact of their submissions.

Table of Contents
Features

Installation

Usage

License

Contributing

Features
Acceptance Prediction
Predicts whether a proposal is likely to be accepted or rejected using a LightGBM classifier trained on thousands of labeled proposals.

Dual Embedding-Based Understanding
Uses both SPECTER and MPNet embeddings to provide a robust semantic understanding of the proposal content.

Top 3 Similar Accepted Proposals
Identifies the top 3 most relevant accepted proposals from a global dataset to help with benchmarking and improvement.

AI-Generated Reviewer Feedback
Generates reviewer-style feedback and improvement suggestions using OpenAI or local language models.

Explainable Predictions (SHAP)
Provides visual explanations for prediction outcomes based on feature contributions, which is optional for users to view.

Flexible Input Options
Supports proposal uploads in .txt, .docx, .pdf formats, or allows users to paste content manually into a clean web UI.

Export as PDF (Coming Soon)
The ability to export feedback and results as a downloadable, formatted PDF report.

Modern Web Interface
A clean, responsive, and user-friendly frontend built using Flask, HTML, CSS, and JavaScript.

Installation
To get started with ProposAI, follow these steps to set up the project locally.

Prerequisites
Python 3.x

Pip (Python package installer)

Clone the repository
bash
Copy
git clone https://github.com/your-username/ProposAI.git
cd ProposAI
Install dependencies
bash
Copy
pip install -r requirements.txt
Running the app
bash
Copy
python app.py
Your application will be running on http://localhost:5000.

Usage
Upload Proposal
Choose a proposal file in .txt, .docx, or .pdf format, or paste the content directly into the web UI.

Receive Feedback
After uploading, the AI will analyze the proposal and provide predictions, feedback, and suggestions.

Review Similar Proposals
The system will also show you the top 3 most relevant accepted proposals for comparison.

Export Results
When available, you can export feedback and results as a PDF.

License
This project is licensed under the MIT License – see the LICENSE file for details.

Contributing
We welcome contributions to ProposAI! If you want to contribute, please follow these steps:

Fork the repository.

Create a new branch (git checkout -b feature-name).

Make your changes.

Commit your changes (git commit -am 'Add feature').

Push to your branch (git push origin feature-name).

Create a new pull request.

Feel free to customize this further based on your specific setup or preferences. Let me know if you'd like additional details!






Ask ChatGPT





ChatGPT can make mista