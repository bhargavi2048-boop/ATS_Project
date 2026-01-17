 📊 Professional ATS Resume Scoring System

The **Professional ATS Resume Scoring System** is an AI-powered web application that evaluates resumes against job descriptions using **Natural Language Processing (NLP)** and **semantic similarity analysis**.  
It helps job seekers understand how well their resumes align with Applicant Tracking Systems (ATS) and provides actionable insights to improve resume quality.

---

## 🚀 Key Features

- Mandatory **Job Role & Job Description validation**
- Upload and analyze **multiple resume PDFs**
- **Overall ATS Match Score** calculation
- **Section-wise resume evaluation**
- **Semantic similarity scoring** using transformer models
- **Skill gap detection** based on job requirements
- **Detailed improvement suggestions**
- **Resume ranking system** for multiple uploads
- **Teal-themed visual score breakdown charts**
- **Professional, multi-section PDF report generation**
- Clean and responsive **Streamlit UI**

---

## 🧠 Advanced Enhancements Added

- Intelligent **skill gap & improvement recommendation engine**
- Automatic **resume ranking leaderboard**
- **Color-coded score interpretation**
- **Compact horizontal bar charts** for better readability
- Enhanced **PDF report design** with charts and workflow diagram
- Strict input validation to prevent incomplete analysis
- Scalable architecture for future ATS integrations

---

## 🛠️ Technology Stack

- **Python 3.10+**
- **Streamlit** – Interactive web interface
- **spaCy** – NLP preprocessing
- **Sentence Transformers** – Semantic similarity computation
- **PyTorch** – Model backend
- **NLTK** – Text cleaning & stopword removal
- **PyPDF2** – Resume PDF text extraction
- **Matplotlib** – Teal-themed data visualizations
- **ReportLab** – Professional PDF report generation

---

## 🔄 System Workflow

1. Select the job role  
2. Paste the job description  
3. Upload one or more resume PDFs  
4. Extract text from resumes  
5. Perform NLP preprocessing  
6. Compute semantic similarity scores  
7. Analyze resumes section-wise  
8. Identify skill gaps & improvement areas  
9. Rank resumes based on ATS score  
10. Generate and download a professional PDF report  

---

## ⚙️ Installation Guide

```bash
pip install streamlit spacy nltk torch sentence-transformers PyPDF2 reportlab matplotlib
python -m spacy download en_core_web_sm

▶️ Run the Application
streamlit run app.py


Access the app at:

http://localhost:8501

📄 Output Generated

Overall ATS match percentage

Technical & soft skill analysis

Skill gap identification

Improvement recommendations

Resume ranking table

Teal-themed visual score charts

Downloadable professional PDF report

✅ Advantages

Improves resume ATS compatibility

Supports multiple resumes at once

Provides actionable career guidance

User-friendly and visually appealing UI

Suitable for academic and professional use

⚠️ Limitations

Accuracy depends on resume text clarity

English-language resumes only

ATS logic is simulated (not company-specific)

🔮 Future Enhancements

Multilingual resume support

Real ATS API integration

Advanced ML-based skill inference

Cloud deployment with user accounts

Recruiter dashboard & analytics

📌 Conclusion

The Professional ATS Resume Scoring System demonstrates the practical use of AI and NLP in modern recruitment.
It serves as a powerful tool for job seekers to optimize resumes, understand ATS behavior, and improve hiring success.

👩‍💻 Author

Bhargavi
Professional ATS Resume Scoring System
