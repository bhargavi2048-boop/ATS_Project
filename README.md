# ATS_Project
ATS Resume Scoring System is a Python-based web application that evaluates resumes against job descriptions using NLP and semantic similarity techniques. It generates an ATS score, identifies matched and missing skills, provides improvement suggestions, and allows users to download a detailed ATS report.
📄 ATS Resume Scoring System

An ATS (Applicant Tracking System) Resume Scoring System built using Python and Natural Language Processing (NLP).
This project analyzes resume PDFs and compares them with job descriptions to generate an ATS compatibility score, identify matched and missing skills, and provide resume improvement suggestions through a user-friendly web interface.

🚀 Project Overview
Modern companies use ATS software to filter resumes before human review.
This project simulates how an ATS works by:

Extracting text from resume PDFs

Cleaning and preprocessing text using NLP

Comparing resumes with job descriptions using semantic similarity

Generating an ATS score (0–100)

Providing skill gap analysis and improvement tips

The application is built using Streamlit, making it easy to use through a web browser.

🛠️ Technologies Used

Python 3.9 – 3.11 – Core programming language

Streamlit – Web application framework

spaCy – NLP processing and tokenization

NLTK – Stopword removal and text preprocessing

Sentence Transformers – Semantic text embeddings

Cosine Similarity – Resume–JD matching

PyPDF2 – Resume PDF text extraction

✨ Key Features

📤 Upload one or multiple resume PDFs

📝 Paste job description

📊 ATS score calculation (0–100)

🧠 Semantic similarity-based matching

🛠️ Skill matching & missing skills detection

📑 Section-wise resume analysis

💡 Resume improvement suggestions

📥 Downloadable ATS analysis report

🎨 Clean and intuitive Streamlit UI

📂 Project Structure
Resume_Scoring_System/
│
├── app.py / Resume_Scoring_System.py
├── requirements.txt
├── README.md
└── assets/
    └── process_flow_diagram.png

⚙️ Installation & Setup
Step 1: Clone the Repository
git clone https://github.com/your-username/ATS-Resume-Scoring-System.git
cd ATS-Resume-Scoring-System

Step 2: Install Required Libraries
pip install streamlit spacy nltk sentence-transformers PyPDF2

Step 3: Download spaCy English Model
python -m spacy download en_core_web_sm

Step 4: Run the Application
streamlit run app.py

Step 5: Open in Browser

The app will open automatically at:

http://localhost:8501

🧪 How to Use

Select the job role

Upload resume PDF(s)

Paste the job description

Click Analyze Resumes

View:

ATS score

Matched & missing skills

Section-wise analysis

Resume improvement suggestions

Download the ATS report

📊 Process Flow Diagram

🎯 Use Cases

Resume screening simulation

Resume optimization for ATS

College mini / final year project

Learning NLP & semantic similarity

Portfolio and interview demonstration

✅ Advantages

Automates resume screening

Saves recruiter time

Helps candidates improve resumes

Beginner-friendly NLP project

Cost-effective and lightweight

🔮 Future Enhancements

Online job portal integration

Advanced skill database

Machine learning-based ranking

Cloud deployment (Streamlit Cloud / AWS)

AI-powered resume rewriting

📌 Conclusion

This ATS Resume Scoring System demonstrates how NLP and semantic similarity can be used to automate resume screening.
It is suitable for students, job seekers, and recruiters who want to understand ATS-based resume evaluation.

🧑‍💻 Author

Bhargavi
📌 College Project | NLP | Python | Streamlit
