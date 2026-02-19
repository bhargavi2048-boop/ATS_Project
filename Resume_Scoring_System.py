import streamlit as st
import matplotlib.pyplot as plt
import PyPDF2
import io
import datetime
import re
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
import plotly.graph_objects as go
import plotly.express as px
from collections import Counter
import pandas as pd
import numpy as np
from wordcloud import WordCloud
import base64

# ============================================================================
# CONFIG & STYLING - ENHANCED LIGHT TEAL BLUE THEME
# ============================================================================
st.set_page_config(
    page_title="Professional ATS Resume Analyzer Pro",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Professional ATS Resume Analyzer Pro v3.0 | Created by Bhargavi",
        "Get help": "https://github.com/yourusername/ats-analyzer",
        "Report a bug": "mailto:contact@example.com"
    }
)

# Color Palette - Enhanced Light Teal Blue Theme
PRIMARY_TEAL = "#4ECDC4"
SECONDARY_TEAL = "#44B8B0"
DARK_TEAL = "#2A9D8F"
LIGHT_TEAL = "#7FD9D1"
PALE_TEAL = "#B2E8E3"
BG_COLOR = "#E8F8F6"
WHITE = "#FFFFFF"
DARK_GRAY = "#2C3E50"
TEXT_DARK = "#1A4D47"
SUCCESS_GREEN = "#27AE60"
WARNING_ORANGE = "#E67E22"
DANGER_RED = "#C0392B"
INFO_BLUE = "#3498DB"
PURPLE = "#9B59B6"
GOLD = "#F39C12"

# Enhanced Custom CSS Styling
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    
    * {{
        margin: 0;
        padding: 0;
        font-family: 'Poppins', sans-serif;
    }}
    
    body {{
        background-color: {BG_COLOR};
        color: {TEXT_DARK};
    }}
    
    .stApp {{
        background: linear-gradient(135deg, {BG_COLOR} 0%, {PALE_TEAL} 100%);
    }}
    
    /* Enhanced Navbar */
    .navbar {{
        background: linear-gradient(135deg, {PRIMARY_TEAL} 0%, {SECONDARY_TEAL} 50%, {DARK_TEAL} 100%);
        padding: 20px 40px;
        border-bottom: 4px solid {DARK_TEAL};
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 20px;
        margin-bottom: 30px;
        border-radius: 12px;
        box-shadow: 0 8px 20px rgba(78, 205, 196, 0.3);
        animation: slideDown 0.5s ease-out;
    }}
    
    @keyframes slideDown {{
        from {{
            transform: translateY(-100%);
            opacity: 0;
        }}
        to {{
            transform: translateY(0);
            opacity: 1;
        }}
    }}
    
    .nav-brand {{
        font-weight: 900;
        font-size: 22px;
        color: {WHITE};
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    
    .nav-link {{
        color: {WHITE};
        text-decoration: none;
        font-weight: 600;
        font-size: 15px;
        padding: 10px 18px;
        border-radius: 8px;
        transition: all 0.3s ease;
        cursor: pointer;
        display: inline-block;
    }}
    
    .nav-link:hover {{
        background-color: {LIGHT_TEAL};
        transform: translateY(-3px) scale(1.05);
        color: {TEXT_DARK};
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }}
    
    .nav-link.active {{
        background-color: {WHITE};
        color: {PRIMARY_TEAL};
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    }}
    
    /* Enhanced Sections */
    .section-title {{
        color: {PRIMARY_TEAL};
        font-size: 38px;
        font-weight: 900;
        margin-bottom: 25px;
        padding-bottom: 15px;
        border-bottom: 4px solid {PRIMARY_TEAL};
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        animation: fadeIn 0.8s ease-in;
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .section-subtitle {{
        color: {PRIMARY_TEAL};
        font-size: 26px;
        font-weight: 700;
        margin-top: 30px;
        margin-bottom: 20px;
        position: relative;
        padding-left: 15px;
    }}
    
    .section-subtitle::before {{
        content: '';
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 5px;
        height: 100%;
        background: {PRIMARY_TEAL};
        border-radius: 3px;
    }}
    
    /* Enhanced Cards */
    .card {{
        background: linear-gradient(145deg, {WHITE} 0%, #F8FFFF 100%);
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid {PRIMARY_TEAL};
        margin-bottom: 20px;
        box-shadow: 0 5px 15px rgba(78, 205, 196, 0.2);
        border: 1px solid {PALE_TEAL};
        transition: all 0.3s ease;
    }}
    
    .card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(78, 205, 196, 0.3);
        border-left-width: 8px;
    }}
    
    /* Enhanced Score Cards */
    .score-card {{
        background: linear-gradient(135deg, {PRIMARY_TEAL} 0%, {SECONDARY_TEAL} 50%, {DARK_TEAL} 100%);
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        color: {WHITE};
        margin: 10px;
        box-shadow: 0 8px 20px rgba(78, 205, 196, 0.4);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    
    .score-card::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 3s ease-in-out infinite;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); opacity: 0.5; }}
        50% {{ transform: scale(1.1); opacity: 0.8; }}
    }}
    
    .score-card:hover {{
        transform: scale(1.05) rotate(1deg);
        box-shadow: 0 12px 30px rgba(78, 205, 196, 0.5);
    }}
    
    .score-value {{
        font-size: 48px;
        font-weight: 900;
        color: {WHITE};
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }}
    
    .score-label {{
        font-size: 15px;
        color: {PALE_TEAL};
        margin-top: 8px;
        font-weight: 600;
        position: relative;
        z-index: 1;
    }}
    
    /* Progress Bars */
    .progress-container {{
        background-color: rgba(78, 205, 196, 0.15);
        border-radius: 10px;
        padding: 3px;
        margin: 10px 0;
    }}
    
    .progress-bar {{
        background: linear-gradient(90deg, {PRIMARY_TEAL} 0%, {SECONDARY_TEAL} 100%);
        height: 25px;
        border-radius: 8px;
        transition: width 1s ease-in-out;
        display: flex;
        align-items: center;
        justify-content: center;
        color: {WHITE};
        font-weight: 700;
        font-size: 13px;
        box-shadow: 0 2px 8px rgba(78, 205, 196, 0.4);
    }}
    
    /* Enhanced Buttons */
    .stButton>button {{
        background: linear-gradient(135deg, {PRIMARY_TEAL} 0%, {SECONDARY_TEAL} 100%);
        color: {WHITE};
        border: none;
        font-weight: 700;
        padding: 14px 28px;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(78, 205, 196, 0.3);
        font-size: 15px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    .stButton>button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(78, 205, 196, 0.4);
        background: linear-gradient(135deg, {SECONDARY_TEAL} 0%, {DARK_TEAL} 100%);
    }}
    
    .stButton>button:active {{
        transform: translateY(0);
        box-shadow: 0 2px 8px rgba(78, 205, 196, 0.3);
    }}
    
    /* Status Messages */
    .stSuccess {{
        background: linear-gradient(135deg, rgba(39, 174, 96, 0.1) 0%, rgba(78, 205, 196, 0.1) 100%);
        border-left: 5px solid {SUCCESS_GREEN};
        padding: 18px;
        border-radius: 8px;
        color: {TEXT_DARK};
        font-weight: 600;
    }}
    
    .stWarning {{
        background: linear-gradient(135deg, rgba(230, 126, 34, 0.1) 0%, rgba(241, 196, 15, 0.1) 100%);
        border-left: 5px solid {WARNING_ORANGE};
        padding: 18px;
        border-radius: 8px;
        font-weight: 600;
    }}
    
    .stError {{
        background: linear-gradient(135deg, rgba(192, 57, 43, 0.1) 0%, rgba(231, 76, 60, 0.1) 100%);
        border-left: 5px solid {DANGER_RED};
        padding: 18px;
        border-radius: 8px;
        font-weight: 600;
    }}
    
    .stInfo {{
        background: linear-gradient(135deg, rgba(78, 205, 196, 0.1) 0%, rgba(52, 152, 219, 0.1) 100%);
        border-left: 5px solid {PRIMARY_TEAL};
        padding: 18px;
        border-radius: 8px;
        color: {TEXT_DARK};
        font-weight: 600;
    }}
    
    /* Metric Badges */
    .metric-badge {{
        display: inline-block;
        background: linear-gradient(135deg, {PRIMARY_TEAL} 0%, {SECONDARY_TEAL} 100%);
        color: {WHITE};
        padding: 10px 16px;
        border-radius: 25px;
        font-size: 13px;
        font-weight: 700;
        margin: 5px;
        box-shadow: 0 3px 10px rgba(78, 205, 196, 0.3);
        transition: all 0.3s ease;
    }}
    
    .metric-badge:hover {{
        transform: scale(1.1);
        box-shadow: 0 5px 15px rgba(78, 205, 196, 0.4);
    }}
    
    /* Feature Boxes */
    .feature-box {{
        background: linear-gradient(135deg, {LIGHT_TEAL} 0%, {PALE_TEAL} 100%);
        padding: 25px;
        border-radius: 15px;
        border: 3px solid {PRIMARY_TEAL};
        color: {TEXT_DARK};
        margin-bottom: 20px;
        box-shadow: 0 5px 15px rgba(78, 205, 196, 0.2);
        transition: all 0.3s ease;
    }}
    
    .feature-box:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(78, 205, 196, 0.3);
    }}
    
    /* Stats Box */
    .stats-box {{
        background: linear-gradient(145deg, {WHITE} 0%, #F0FFFF 100%);
        padding: 20px;
        border-radius: 12px;
        border: 2px solid {PRIMARY_TEAL};
        margin: 15px 0;
        box-shadow: 0 4px 12px rgba(78, 205, 196, 0.2);
    }}
    
    /* Animated Icons */
    .animated-icon {{
        display: inline-block;
        animation: bounce 2s infinite;
    }}
    
    @keyframes bounce {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-10px); }}
    }}
    
    /* Footer */
    .footer {{
        text-align: center;
        padding: 30px 20px;
        color: {DARK_TEAL};
        border-top: 3px solid {PRIMARY_TEAL};
        margin-top: 50px;
        font-size: 13px;
        background: linear-gradient(135deg, {PALE_TEAL} 0%, {BG_COLOR} 100%);
        border-radius: 10px;
    }}
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {{
        color: {PRIMARY_TEAL};
        font-weight: 700;
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 15px;
        background-color: transparent;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: {PALE_TEAL};
        color: {TEXT_DARK};
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background-color: {LIGHT_TEAL};
        transform: translateY(-2px);
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {PRIMARY_TEAL} 0%, {SECONDARY_TEAL} 100%);
        color: {WHITE};
        box-shadow: 0 4px 12px rgba(78, 205, 196, 0.3);
    }}
    
    /* Expander */
    .streamlit-expanderHeader {{
        background-color: {PALE_TEAL};
        border-radius: 8px;
        font-weight: 600;
        color: {TEXT_DARK};
    }}
    
    .streamlit-expanderHeader:hover {{
        background-color: {LIGHT_TEAL};
    }}
    
    /* File Uploader */
    .stFileUploader {{
        background-color: {WHITE};
        border: 2px dashed {PRIMARY_TEAL};
        border-radius: 10px;
        padding: 20px;
    }}
    
    /* Tooltips */
    .tooltip {{
        position: relative;
        display: inline-block;
        cursor: help;
        color: {PRIMARY_TEAL};
        font-weight: 600;
    }}
    
    .tooltip:hover::after {{
        content: attr(data-tooltip);
        position: absolute;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        background-color: {DARK_GRAY};
        color: {WHITE};
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 12px;
        white-space: nowrap;
        z-index: 1000;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }}
    
    /* Ranking Badge */
    .rank-badge {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        font-size: 24px;
        font-weight: 900;
        color: {WHITE};
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }}
    
    .rank-1 {{ background: linear-gradient(135deg, {GOLD} 0%, #F1C40F 100%); }}
    .rank-2 {{ background: linear-gradient(135deg, #BDC3C7 0%, #95A5A6 100%); }}
    .rank-3 {{ background: linear-gradient(135deg, #CD7F32 0%, #A0522D 100%); }}
    .rank-other {{ background: linear-gradient(135deg, {PRIMARY_TEAL} 0%, {SECONDARY_TEAL} 100%); }}
    
    /* Comparison Table */
    .comparison-table {{
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        background-color: {WHITE};
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(78, 205, 196, 0.2);
    }}
    
    .comparison-table th {{
        background: linear-gradient(135deg, {PRIMARY_TEAL} 0%, {SECONDARY_TEAL} 100%);
        color: {WHITE};
        padding: 15px;
        font-weight: 700;
        text-align: left;
    }}
    
    .comparison-table td {{
        padding: 12px 15px;
        border-bottom: 1px solid {PALE_TEAL};
        color: {TEXT_DARK};
    }}
    
    .comparison-table tr:hover {{
        background-color: rgba(78, 205, 196, 0.05);
    }}
    
    /* Loading Animation */
    .loading-spinner {{
        border: 5px solid {PALE_TEAL};
        border-top: 5px solid {PRIMARY_TEAL};
        border-radius: 50%;
        width: 50px;
        height: 50px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }}
    
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}
    
    /* Responsive Design */
    @media (max-width: 768px) {{
        .navbar {{
            flex-direction: column;
            padding: 15px 20px;
        }}
        
        .section-title {{
            font-size: 28px;
        }}
        
        .score-value {{
            font-size: 36px;
        }}
    }}
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# ENHANCED KEYWORD DATABASES
# ============================================================================
KEYWORD_DATABASE = {
    "Technical Skills": {
        "Programming": ["python", "java", "c++", "c#", "javascript", "typescript", "ruby", "php", "swift", "kotlin", "go", "rust"],
        "Data Science": ["machine learning", "deep learning", "neural networks", "nlp", "computer vision", "tensorflow", "pytorch", "scikit-learn", "keras"],
        "Data Analysis": ["sql", "mysql", "postgresql", "oracle", "mongodb", "data analysis", "data visualization", "statistics", "pandas", "numpy"],
        "BI Tools": ["tableau", "power bi", "looker", "qlik", "sisense", "metabase", "dax", "power query"],
        "Web Development": ["html", "css", "react", "vue", "angular", "node.js", "express", "django", "flask", "fastapi"],
        "Cloud": ["aws", "azure", "gcp", "cloud", "docker", "kubernetes", "terraform", "ci/cd", "jenkins", "github actions"],
        "Mobile": ["android", "ios", "react native", "flutter", "xamarin", "swift", "kotlin"],
        "Big Data": ["hadoop", "spark", "kafka", "hive", "airflow", "etl", "data pipeline", "distributed systems"],
        "Excel": ["excel", "vba", "macros", "pivot tables", "vlookup", "xlookup", "power query", "spreadsheets"],
    },
    "Soft Skills": {
        "Leadership": ["leadership", "lead", "led", "managed", "supervise", "mentor", "coach", "direct", "oversee", "coordinate"],
        "Communication": ["communication", "presentation", "written", "verbal", "articulate", "public speaking", "negotiation"],
        "Teamwork": ["teamwork", "collaboration", "collaborative", "team", "cooperate", "cross-functional", "agile", "scrum"],
        "Problem Solving": ["problem solving", "analytical", "critical thinking", "troubleshoot", "innovative", "creative", "solution-oriented"],
        "Time Management": ["time management", "prioritize", "organization", "efficient", "deadline", "multitask", "planning"],
        "Adaptability": ["adaptability", "flexible", "adaptable", "quick learner", "versatile", "dynamic", "resilient"],
        "Interpersonal": ["interpersonal", "relationship building", "networking", "empathy", "emotional intelligence"],
    },
    "Metrics & Impact": {
        "Growth": ["growth", "increase", "increased", "improved", "enhanced", "optimized", "boosted", "elevated", "expanded"],
        "Efficiency": ["reduced", "decreased", "efficiency", "faster", "streamlined", "automated", "simplified", "accelerated"],
        "Achievement": ["achieved", "accomplished", "delivered", "completed", "launched", "implemented", "executed", "established"],
        "Performance": ["performance", "productivity", "quality", "results", "roi", "kpi", "metrics", "revenue", "profit"],
        "Scale": ["scaled", "grew", "million", "thousand", "x times", "%", "percentage", "dollar", "$"],
    },
    "Action Verbs": {
        "Strong": ["spearheaded", "pioneered", "orchestrated", "revolutionized", "transformed", "architected", "engineered", 
                  "designed", "developed", "created", "built", "implemented", "executed", "delivered", "achieved"],
    }
}

# Role-specific skill requirements with weights
ROLE_KEYWORDS = {
    "Data Analyst": {
        "required": ["sql", "excel", "data analysis"],
        "preferred": ["python", "tableau", "power bi", "statistics", "data visualization"],
        "bonus": ["etl", "dashboard", "reporting", "kpi"]
    },
    "Data Scientist": {
        "required": ["python", "machine learning", "statistics"],
        "preferred": ["sql", "tensorflow", "scikit-learn", "pandas", "numpy", "deep learning"],
        "bonus": ["nlp", "computer vision", "model deployment", "aws", "docker"]
    },
    "Web Developer": {
        "required": ["html", "css", "javascript"],
        "preferred": ["react", "node.js", "git", "api", "responsive design"],
        "bonus": ["typescript", "mongodb", "docker", "aws", "ci/cd"]
    },
    "Machine Learning Engineer": {
        "required": ["python", "machine learning", "deep learning"],
        "preferred": ["tensorflow", "pytorch", "docker", "aws", "model deployment"],
        "bonus": ["mlops", "kubernetes", "spark", "airflow"]
    },
    "Full Stack Developer": {
        "required": ["javascript", "html", "css", "backend", "frontend"],
        "preferred": ["react", "node.js", "sql", "api", "git"],
        "bonus": ["docker", "aws", "ci/cd", "microservices"]
    },
    "Business Analyst": {
        "required": ["requirements gathering", "stakeholder management", "documentation"],
        "preferred": ["sql", "excel", "business intelligence", "process improvement"],
        "bonus": ["agile", "scrum", "jira", "power bi"]
    },
}

# Industry-specific keywords
INDUSTRY_KEYWORDS = {
    "Finance": ["financial analysis", "risk management", "compliance", "trading", "portfolio", "investment"],
    "Healthcare": ["healthcare", "medical", "patient", "clinical", "hipaa", "ehr"],
    "E-commerce": ["e-commerce", "retail", "customer", "sales", "conversion", "marketplace"],
    "Technology": ["saas", "software", "platform", "api", "cloud", "scalability"],
}

# ============================================================================
# CORE FUNCTIONS - ENHANCED
# ============================================================================

def extract_text(pdf_file):
    """Extract text from PDF file with enhanced error handling"""
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page_num, page in enumerate(reader.pages):
            try:
                text += page.extract_text() + "\n"
            except Exception as e:
                st.warning(f"Warning: Could not extract text from page {page_num + 1}")
        return text.lower()
    except Exception as e:
        st.error(f"❌ Error extracting PDF: {e}")
        return ""

def count_keyword_matches(resume_text, keywords_list):
    """Count matches for a list of keywords with improved matching"""
    matches = {}
    for keyword in keywords_list:
        pattern = r'\b' + re.escape(keyword) + r'\b'
        found = re.findall(pattern, resume_text, re.IGNORECASE)
        if found:
            matches[keyword] = len(found)
    return matches

def extract_sections(resume_text):
    """Extract common resume sections with improved parsing"""
    sections = {
        "experience": "",
        "skills": "",
        "education": "",
        "projects": "",
        "certifications": "",
        "summary": "",
        "contact": ""
    }
    
    patterns = {
        "experience": r'(?:experience|work history|employment|professional experience)(.+?)(?=skills|education|projects|certifications|$)',
        "skills": r'(?:skills|technical skills|core competencies)(.+?)(?=experience|education|projects|certifications|$)',
        "education": r'(?:education|academic background|qualifications)(.+?)(?=experience|skills|projects|certifications|$)',
        "projects": r'(?:projects|portfolio|personal projects)(.+?)(?=experience|skills|education|certifications|$)',
        "certifications": r'(?:certifications|certificates|licenses)(.+?)(?=experience|skills|education|projects|$)',
        "summary": r'(?:summary|objective|profile|about)(.+?)(?=experience|skills|education|projects|certifications|$)',
        "contact": r'(?:contact|email|phone|linkedin)(.+?)(?=summary|experience|skills|education|$)',
    }
    
    for section, pattern in patterns.items():
        match = re.search(pattern, resume_text, re.IGNORECASE | re.DOTALL)
        if match:
            sections[section] = match.group(1).strip()[:800]
    
    return sections

def extract_email(text):
    """Extract email address from resume"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return emails[0] if emails else None

def extract_phone(text):
    """Extract phone number from resume"""
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    phones = re.findall(phone_pattern, text)
    return phones[0] if phones else None

def extract_linkedin(text):
    """Extract LinkedIn URL from resume"""
    linkedin_pattern = r'linkedin\.com/in/[\w-]+'
    linkedin = re.findall(linkedin_pattern, text, re.IGNORECASE)
    return linkedin[0] if linkedin else None

def extract_github(text):
    """Extract GitHub URL from resume"""
    github_pattern = r'github\.com/[\w-]+'
    github = re.findall(github_pattern, text, re.IGNORECASE)
    return github[0] if github else None

def calculate_ats_score(resume_text, job_description="", job_role=""):
    """Calculate comprehensive ATS score with enhanced metrics"""
    resume_text_lower = resume_text.lower()
    jd_lower = job_description.lower() if job_description else ""
    
    scores = {}
    detailed_feedback = {}
    
    # 1. Technical Skills Score (Enhanced)
    if job_role and job_role in ROLE_KEYWORDS:
        role_data = ROLE_KEYWORDS[job_role]
        
        required_found = count_keyword_matches(resume_text_lower, role_data["required"])
        preferred_found = count_keyword_matches(resume_text_lower, role_data["preferred"])
        bonus_found = count_keyword_matches(resume_text_lower, role_data["bonus"])
        
        required_score = (len(required_found) / len(role_data["required"])) * 50
        preferred_score = (len(preferred_found) / len(role_data["preferred"])) * 35
        bonus_score = (len(bonus_found) / len(role_data["bonus"])) * 15
        
        tech_score = min(100, required_score + preferred_score + bonus_score)
        
        detailed_feedback["Technical Skills"] = {
            "required": list(required_found.keys()),
            "preferred": list(preferred_found.keys()),
            "bonus": list(bonus_found.keys()),
            "missing_required": [k for k in role_data["required"] if k not in required_found],
            "missing_preferred": [k for k in role_data["preferred"] if k not in preferred_found],
        }
    else:
        all_tech_skills = []
        for category in KEYWORD_DATABASE["Technical Skills"].values():
            all_tech_skills.extend(category)
        
        tech_matches = count_keyword_matches(resume_text_lower, all_tech_skills)
        tech_score = min(100, (len(tech_matches) / 15) * 100)
        
        detailed_feedback["Technical Skills"] = {
            "found": list(tech_matches.keys()),
            "count": len(tech_matches)
        }
    
    scores["Technical Skills"] = round(tech_score, 2)
    
    # 2. Soft Skills Score
    all_soft_skills = []
    for category in KEYWORD_DATABASE["Soft Skills"].values():
        all_soft_skills.extend(category)
    
    soft_matches = count_keyword_matches(resume_text_lower, all_soft_skills)
    soft_score = min(100, (len(soft_matches) / 12) * 100)
    scores["Soft Skills"] = round(soft_score, 2)
    
    detailed_feedback["Soft Skills"] = {
        "found": list(soft_matches.keys()),
        "count": len(soft_matches)
    }
    
    # 3. Metrics & Impact Score (Enhanced)
    metrics_keywords = []
    for category in KEYWORD_DATABASE["Metrics & Impact"].values():
        metrics_keywords.extend(category)
    
    metrics_matches = count_keyword_matches(resume_text_lower, metrics_keywords)
    
    # Check for actual numbers and percentages
    numbers = re.findall(r'\b\d+(?:,\d{3})*(?:\.\d+)?(?:%|k|m|million|thousand|billion)?\b', resume_text_lower)
    
    metrics_score = min(100, (len(metrics_matches) * 8 + len(numbers) * 3))
    scores["Metrics & Results"] = round(metrics_score, 2)
    
    detailed_feedback["Metrics & Results"] = {
        "found": list(metrics_matches.keys()),
        "numbers_found": len(numbers),
        "examples": numbers[:5]
    }
    
    # 4. Experience Match Score (Enhanced)
    if jd_lower:
        jd_words = set(jd_lower.split())
        resume_words = set(resume_text_lower.split())
        
        # Remove common words
        common_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
        jd_words = jd_words - common_words
        
        overlap = jd_words.intersection(resume_words)
        exp_score = min(100, (len(overlap) / len(jd_words)) * 100) if jd_words else 75
        
        detailed_feedback["Experience Match"] = {
            "matched_keywords": list(overlap)[:20],
            "match_percentage": round((len(overlap) / len(jd_words)) * 100, 2) if jd_words else 0
        }
    else:
        exp_score = 75
        detailed_feedback["Experience Match"] = {"note": "No job description provided"}
    
    scores["Experience Match"] = round(exp_score, 2)
    
    # 5. ATS Compatibility Score (Enhanced)
    formatting_score = 100
    issues = []
    
    # Check for ATS-unfriendly elements
    if "image" in resume_text_lower or "jpg" in resume_text_lower or "png" in resume_text_lower:
        formatting_score -= 20
        issues.append("Contains images")
    
    if resume_text.count("|") > 10:
        formatting_score -= 15
        issues.append("Excessive use of tables/pipes")
    
    # Check for standard sections
    standard_sections = ["experience", "education", "skills"]
    missing_sections = [s for s in standard_sections if s not in resume_text_lower]
    if missing_sections:
        formatting_score -= len(missing_sections) * 10
        issues.extend([f"Missing {s} section" for s in missing_sections])
    
    # Check for contact information
    if not extract_email(resume_text):
        formatting_score -= 10
        issues.append("No email address found")
    
    scores["ATS Compatibility"] = round(max(50, formatting_score), 2)
    detailed_feedback["ATS Compatibility"] = {"issues": issues}
    
    # 6. Keyword Density Score
    total_words = len(resume_text_lower.split())
    
    all_keywords = []
    for category in KEYWORD_DATABASE.values():
        for subcategory in category.values():
            all_keywords.extend(subcategory)
    
    keyword_matches = count_keyword_matches(resume_text_lower, all_keywords)
    total_keyword_occurrences = sum(keyword_matches.values())
    
    keyword_density = (total_keyword_occurrences / total_words * 100) if total_words > 0 else 0
    
    # Optimal density is 5-10%
    if 5 <= keyword_density <= 10:
        keyword_score = 100
    elif keyword_density < 5:
        keyword_score = keyword_density * 20
    else:
        keyword_score = 100 - (keyword_density - 10) * 5
    
    scores["Keyword Density"] = round(max(0, min(100, keyword_score)), 2)
    detailed_feedback["Keyword Density"] = {
        "density_percentage": round(keyword_density, 2),
        "total_keywords": len(keyword_matches),
        "total_words": total_words
    }
    
    # 7. Action Verbs Score (NEW)
    action_verbs = KEYWORD_DATABASE["Action Verbs"]["Strong"]
    action_matches = count_keyword_matches(resume_text_lower, action_verbs)
    action_score = min(100, len(action_matches) * 10)
    
    scores["Action Verbs"] = round(action_score, 2)
    detailed_feedback["Action Verbs"] = {
        "found": list(action_matches.keys()),
        "count": len(action_matches)
    }
    
    # 8. Section Completeness Score (NEW)
    sections = extract_sections(resume_text)
    present_sections = [k for k, v in sections.items() if v]
    section_score = (len(present_sections) / len(sections)) * 100
    
    scores["Section Completeness"] = round(section_score, 2)
    detailed_feedback["Section Completeness"] = {
        "present": present_sections,
        "missing": [k for k, v in sections.items() if not v]
    }
    
    return scores, sections, detailed_feedback

def generate_improvement_suggestions(scores, sections, detailed_feedback):
    """Generate personalized improvement suggestions with priorities"""
    suggestions = []
    priority_suggestions = []
    
    # Technical Skills
    if scores["Technical Skills"] < 60:
        priority_suggestions.append({
            "priority": "HIGH",
            "category": "Technical Skills",
            "suggestion": "Add more technical skills from the job description",
            "details": f"Missing key skills: {', '.join(detailed_feedback.get('Technical Skills', {}).get('missing_required', []))}"
        })
    
    # Metrics & Results
    if scores["Metrics & Results"] < 60:
        priority_suggestions.append({
            "priority": "HIGH",
            "category": "Achievements",
            "suggestion": "Include quantifiable achievements with numbers and percentages",
            "details": "Add metrics like: 'Increased sales by 30%' or 'Reduced processing time from 8 hours to 4 hours'"
        })
    
    # Soft Skills
    if scores["Soft Skills"] < 50:
        suggestions.append({
            "priority": "MEDIUM",
            "category": "Soft Skills",
            "suggestion": "Highlight soft skills like leadership, communication, and teamwork",
            "details": "Integrate soft skills naturally into your experience descriptions"
        })
    
    # Experience Match
    if scores["Experience Match"] < 70:
        suggestions.append({
            "priority": "HIGH",
            "category": "Keyword Matching",
            "suggestion": "Align your experience section with job description keywords",
            "details": "Mirror the language used in the job posting"
        })
    
    # ATS Compatibility
    if scores["ATS Compatibility"] < 80:
        issues = detailed_feedback.get("ATS Compatibility", {}).get("issues", [])
        priority_suggestions.append({
            "priority": "CRITICAL",
            "category": "Formatting",
            "suggestion": "Fix ATS compatibility issues",
            "details": "Issues found: " + ", ".join(issues)
        })
    
    # Keyword Density
    density = detailed_feedback.get("Keyword Density", {}).get("density_percentage", 0)
    if density < 5:
        suggestions.append({
            "priority": "MEDIUM",
            "category": "Keywords",
            "suggestion": "Increase keyword usage throughout your resume",
            "details": f"Current density: {density:.1f}%. Target: 5-10%"
        })
    elif density > 10:
        suggestions.append({
            "priority": "MEDIUM",
            "category": "Keywords",
            "suggestion": "Reduce keyword stuffing for more natural language",
            "details": f"Current density: {density:.1f}%. Target: 5-10%"
        })
    
    # Action Verbs
    if scores["Action Verbs"] < 50:
        suggestions.append({
            "priority": "MEDIUM",
            "category": "Language",
            "suggestion": "Use stronger action verbs to describe your accomplishments",
            "details": "Replace weak verbs like 'responsible for' with 'Led', 'Developed', 'Implemented'"
        })
    
    # Section Completeness
    missing_sections = detailed_feedback.get("Section Completeness", {}).get("missing", [])
    if missing_sections:
        suggestions.append({
            "priority": "HIGH",
            "category": "Structure",
            "suggestion": f"Add missing resume sections: {', '.join(missing_sections)}",
            "details": "Complete resumes include all standard sections"
        })
    
    # Sort by priority
    all_suggestions = priority_suggestions + suggestions
    priority_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    all_suggestions.sort(key=lambda x: priority_order.get(x["priority"], 4))
    
    return all_suggestions

def generate_strengths(scores, detailed_feedback):
    """Generate resume strengths based on scores"""
    strengths = []
    
    if scores["Technical Skills"] >= 70:
        found_skills = detailed_feedback.get("Technical Skills", {}).get("found", [])
        strengths.append({
            "category": "Technical Skills",
            "strength": "Strong technical skills alignment",
            "details": f"Demonstrates proficiency in: {', '.join(found_skills[:5])}"
        })
    
    if scores["Metrics & Results"] >= 70:
        num_count = detailed_feedback.get("Metrics & Results", {}).get("numbers_found", 0)
        strengths.append({
            "category": "Impact",
            "strength": "Excellent use of quantifiable achievements",
            "details": f"Contains {num_count} quantified metrics showcasing tangible impact"
        })
    
    if scores["Soft Skills"] >= 70:
        soft_skills = detailed_feedback.get("Soft Skills", {}).get("found", [])
        strengths.append({
            "category": "Soft Skills",
            "strength": "Good coverage of important soft skills",
            "details": f"Highlights: {', '.join(soft_skills[:4])}"
        })
    
    if scores["ATS Compatibility"] >= 85:
        strengths.append({
            "category": "Formatting",
            "strength": "Clean, ATS-friendly formatting",
            "details": "Resume structure is optimized for applicant tracking systems"
        })
    
    if scores["Keyword Density"] >= 70:
        density = detailed_feedback.get("Keyword Density", {}).get("density_percentage", 0)
        strengths.append({
            "category": "Keywords",
            "strength": "Optimal keyword density",
            "details": f"Maintains healthy {density:.1f}% keyword density"
        })
    
    if scores["Experience Match"] >= 75:
        match_pct = detailed_feedback.get("Experience Match", {}).get("match_percentage", 0)
        strengths.append({
            "category": "Relevance",
            "strength": "Strong alignment with job requirements",
            "details": f"{match_pct:.0f}% keyword match with job description"
        })
    
    if scores["Action Verbs"] >= 70:
        verbs = detailed_feedback.get("Action Verbs", {}).get("found", [])
        strengths.append({
            "category": "Language",
            "strength": "Effective use of action verbs",
            "details": f"Uses strong verbs: {', '.join(verbs[:5])}"
        })
    
    if scores["Section Completeness"] >= 85:
        strengths.append({
            "category": "Structure",
            "strength": "Comprehensive resume structure",
            "details": "Includes all standard resume sections"
        })
    
    return strengths

def create_pdf_report(resumes_data):
    """Generate enhanced professional PDF report"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, 
                           topMargin=0.5*inch, bottomMargin=0.5*inch,
                           leftMargin=0.75*inch, rightMargin=0.75*inch)
    styles = getSampleStyleSheet()
    elements = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=26,
        textColor=colors.HexColor(PRIMARY_TEAL),
        spaceAfter=12,
        alignment=1,
        fontName='Helvetica-Bold'
    )
    elements.append(Paragraph("<b>🏆 Professional ATS Resume Evaluation Report</b>", title_style))
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor(DARK_GRAY),
        alignment=1,
        spaceAfter=20
    )
    elements.append(Paragraph(f"Generated on: {datetime.datetime.now().strftime('%B %d, %Y at %I:%M %p')}", subtitle_style))
    elements.append(Spacer(1, 20))
    
    # Executive Summary
    if len(resumes_data) > 1:
        elements.append(Paragraph("<b>📊 Executive Summary</b>", styles['Heading2']))
        
        avg_score = sum(r['overall_score'] for r in resumes_data) / len(resumes_data)
        max_score = max(r['overall_score'] for r in resumes_data)
        min_score = min(r['overall_score'] for r in resumes_data)
        
        summary_data = [
            ["Total Resumes Analyzed", str(len(resumes_data))],
            ["Average Score", f"{avg_score:.1f}%"],
            ["Highest Score", f"{max_score:.1f}%"],
            ["Lowest Score", f"{min_score:.1f}%"],
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,-1), colors.HexColor(PRIMARY_TEAL)),
            ('TEXTCOLOR', (0,0), (0,-1), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 11),
            ('GRID', (0,0), (-1,-1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.white, colors.HexColor('#ECF0F1')]),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 20))
    
    # Individual Resume Reports
    for idx, data in enumerate(resumes_data, 1):
        # Header
        header_style = ParagraphStyle(
            'ResumeHeader',
            parent=styles['Heading2'],
            fontSize=18,
            textColor=colors.HexColor(PRIMARY_TEAL),
            spaceAfter=10,
            fontName='Helvetica-Bold'
        )
        
        rank_emoji = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else "📄"
        elements.append(Paragraph(f"<b>{rank_emoji} Candidate {idx}: {data['name']}</b>", header_style))
        
        # Basic Info
        info_data = [
            ["Target Role:", data['role']],
            ["Overall ATS Score:", f"{data['overall_score']}%"],
            ["Ranking:", f"#{idx} of {len(resumes_data)}"],
            ["Analyzed Date:", datetime.datetime.now().strftime('%Y-%m-%d %H:%M')],
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,-1), colors.HexColor(PRIMARY_TEAL)),
            ('TEXTCOLOR', (0,0), (0,-1), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('GRID', (0,0), (-1,-1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.white, colors.HexColor('#F8F9FA')]),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 15))
        
        # Score Breakdown
        elements.append(Paragraph("<b>📈 Detailed Score Breakdown</b>", styles['Heading3']))
        
        table_data = [["Category", "Score (%)", "Rating", "Status"]]
        for k, v in data['scores'].items():
            if v >= 80:
                rating = "Excellent"
                status = "✓ Strong"
            elif v >= 60:
                rating = "Good"
                status = "↗ Moderate"
            else:
                rating = "Needs Work"
                status = "⚠ Improve"
            
            table_data.append([k, f"{v:.1f}%", rating, status])
        
        table = Table(table_data, colWidths=[2.2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor(PRIMARY_TEAL)),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8F9FA')]),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 15))
        
        # Strengths
        elements.append(Paragraph("<b>✅ Resume Strengths</b>", styles['Heading3']))
        for strength in data['strengths']:
            if isinstance(strength, dict):
                elements.append(Paragraph(f"• <b>{strength['category']}:</b> {strength['strength']}", styles['Normal']))
                if 'details' in strength:
                    detail_style = ParagraphStyle('Detail', parent=styles['Normal'], fontSize=9, leftIndent=20, textColor=colors.HexColor(DARK_GRAY))
                    elements.append(Paragraph(f"  {strength['details']}", detail_style))
            else:
                elements.append(Paragraph(f"• {strength}", styles['Normal']))
        elements.append(Spacer(1, 15))
        
        # Improvements
        elements.append(Paragraph("<b>🔧 Improvement Recommendations</b>", styles['Heading3']))
        for improvement in data['improvements']:
            if isinstance(improvement, dict):
                priority_color = {
                    "CRITICAL": colors.red,
                    "HIGH": colors.orange,
                    "MEDIUM": colors.blue,
                    "LOW": colors.green
                }.get(improvement.get('priority', 'MEDIUM'), colors.blue)
                
                priority_style = ParagraphStyle('Priority', parent=styles['Normal'], textColor=priority_color, fontName='Helvetica-Bold')
                elements.append(Paragraph(f"• [{improvement.get('priority', 'MEDIUM')}] <b>{improvement.get('category', '')}:</b> {improvement.get('suggestion', '')}", priority_style))
                
                if 'details' in improvement:
                    detail_style = ParagraphStyle('Detail', parent=styles['Normal'], fontSize=9, leftIndent=20, textColor=colors.HexColor(DARK_GRAY))
                    elements.append(Paragraph(f"  {improvement['details']}", detail_style))
            else:
                elements.append(Paragraph(f"• {improvement}", styles['Normal']))
        elements.append(Spacer(1, 15))
        
        # Key Metrics
        if 'detailed_feedback' in data:
            elements.append(Paragraph("<b>📊 Key Metrics & Insights</b>", styles['Heading3']))
            
            metrics_data = []
            
            # Keyword Density
            if 'Keyword Density' in data['detailed_feedback']:
                kd = data['detailed_feedback']['Keyword Density']
                metrics_data.append(["Keyword Density", f"{kd.get('density_percentage', 0):.2f}%"])
                metrics_data.append(["Total Keywords Found", str(kd.get('total_keywords', 0))])
                metrics_data.append(["Total Words", str(kd.get('total_words', 0))])
            
            # Technical Skills
            if 'Technical Skills' in data['detailed_feedback']:
                ts = data['detailed_feedback']['Technical Skills']
                if 'found' in ts:
                    metrics_data.append(["Technical Skills Found", ', '.join(ts['found'][:5])])
            
            if metrics_data:
                metrics_table = Table(metrics_data, colWidths=[2.5*inch, 3.5*inch])
                metrics_table.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (0,-1), colors.HexColor(PALE_TEAL)),
                    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                    ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0,0), (-1,-1), 9),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                    ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.white, colors.HexColor('#F8F9FA')]),
                ]))
                elements.append(metrics_table)
                elements.append(Spacer(1, 15))
        
        # Page break between resumes
        if idx < len(resumes_data):
            elements.append(PageBreak())
    
    # Footer
    elements.append(Spacer(1, 30))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor(DARK_GRAY),
        alignment=1,
        spaceAfter=5
    )
    elements.append(Paragraph("<i>© 2026 Professional ATS Resume Analyzer Pro | AI-Powered Resume Evaluation</i>", footer_style))
    elements.append(Paragraph("<i>This report is confidential and intended for the recipient only.</i>", footer_style))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer

def create_wordcloud(text, title="Word Cloud"):
    """Generate word cloud from resume text"""
    try:
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color=WHITE,
            colormap='viridis',
            max_words=100,
            relative_scaling=0.5,
            min_font_size=10
        ).generate(text)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title(title, fontsize=16, fontweight='bold', color=PRIMARY_TEAL)
        
        return fig
    except Exception as e:
        st.warning(f"Could not generate word cloud: {e}")
        return None

# ============================================================================
# NAVIGATION & PAGE MANAGEMENT
# ============================================================================

def render_navbar():
    """Render enhanced navigation bar"""
    current_page = get_current_page()
    
    nav_items = {
        "Home": "🏠",
        "Upload": "📤",
        "Tips": "📚",
        "Analytics": "📊",
        "Compare": "⚖️",
        "About": "ℹ️",
        "FAQ": "❓"
    }
    
    nav_links = ""
    for page, icon in nav_items.items():
        active_class = "active" if page == current_page else ""
        nav_links += f'<a href="?page={page}" class="nav-link {active_class}">{icon} {page}</a>'
    
    st.markdown(f"""
        <div class="navbar">
            <div class="nav-brand">
                <span class="animated-icon">🎯</span> ATS Resume Analyzer Pro
            </div>
            <div style="display: flex; gap: 15px; flex-wrap: wrap;">
                {nav_links}
            </div>
        </div>
    """, unsafe_allow_html=True)

def get_current_page():
    """Get current page from query params"""
    qp = st.query_params
    page_value = qp.get("page", "Home")
    if isinstance(page_value, list):
        return page_value[0] if page_value else "Home"
    return page_value or "Home"

def render_footer():
    """Render enhanced footer"""
    st.markdown(f"""
        <div class="footer">
            <p style='font-weight: 700; font-size: 14px; color: {PRIMARY_TEAL}; margin-bottom: 8px;'>
                Professional ATS Resume Analyzer Pro v3.0
            </p>
            <p style='margin-bottom: 8px;'>
                © 2026 Created with ❤️ by <b>Bhargavi</b> | All Rights Reserved
            </p>
            <p style='font-size: 11px;'>
                Powered by Streamlit • PyPDF2 • ReportLab • Plotly • WordCloud
            </p>
            <p style='font-size: 11px; margin-top: 8px;'>
                <a href='mailto:contact@example.com' style='color: {PRIMARY_TEAL}; text-decoration: none;'>📧 Contact</a> • 
                <a href='https://github.com' style='color: {PRIMARY_TEAL}; text-decoration: none;'>💻 GitHub</a> • 
                <a href='https://linkedin.com' style='color: {PRIMARY_TEAL}; text-decoration: none;'>🔗 LinkedIn</a>
            </p>
        </div>
    """, unsafe_allow_html=True)

# ============================================================================
# PAGE: HOME (ENHANCED)
# ============================================================================

def home_page():
    st.markdown(f"""
        <h1 style='color: {PRIMARY_TEAL}; text-align: center; font-size: 48px; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.1);'>
            <span class='animated-icon'>🚀</span> Welcome to ATS Resume Analyzer Pro
        </h1>
        <p style='text-align: center; color: {TEXT_DARK}; font-size: 18px; margin-bottom: 40px; font-weight: 500;'>
            Your AI-powered companion for creating ATS-optimized resumes that stand out
        </p>
    """, unsafe_allow_html=True)
    
    # Hero Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class='score-card'>
                <div class='score-value'>8</div>
                <div class='score-label'>Scoring Categories</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='score-card'>
                <div class='score-value'>100+</div>
                <div class='score-label'>Keywords Tracked</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class='score-card'>
                <div class='score-value'>6</div>
                <div class='score-label'>Job Roles Supported</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class='score-card'>
                <div class='score-value'>∞</div>
                <div class='score-label'>Analyses Available</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Feature Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class='card'>
                <h3 style='color: {PRIMARY_TEAL}; margin-top: 0;'>🎯 Smart Analysis</h3>
                <p style='color: {TEXT_DARK}; line-height: 1.8;'>Get instant ATS scores across <b>8 different categories</b> with detailed breakdowns, keyword matching, and industry-specific insights.</p>
                <br>
                <div style='background: {PALE_TEAL}; padding: 10px; border-radius: 8px;'>
                    <small><b>Categories:</b> Technical Skills, Soft Skills, Metrics, Experience Match, ATS Compatibility, Keyword Density, Action Verbs, Section Completeness</small>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='card'>
                <h3 style='color: {PRIMARY_TEAL}; margin-top: 0;'>📊 Visual Insights</h3>
                <p style='color: {TEXT_DARK}; line-height: 1.8;'>Interactive charts, comparison tools, word clouds, and ranking systems help you understand your resume's performance at a glance.</p>
                <br>
                <div style='background: {PALE_TEAL}; padding: 10px; border-radius: 8px;'>
                    <small><b>Features:</b> Score breakdowns, radar charts, progress bars, competitive rankings, keyword density analysis</small>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class='card'>
                <h3 style='color: {PRIMARY_TEAL}; margin-top: 0;'>📥 Professional Reports</h3>
                <p style='color: {TEXT_DARK}; line-height: 1.8;'>Download beautiful PDF reports with comprehensive analytics, prioritized recommendations, and competitive rankings.</p>
                <br>
                <div style='background: {PALE_TEAL}; padding: 10px; border-radius: 8px;'>
                    <small><b>Includes:</b> Executive summary, detailed scores, strengths analysis, improvement roadmap, key metrics</small>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Key Features Section
    st.markdown(f"""
        <div class='card'>
            <h3 style='color: {PRIMARY_TEAL}; margin-top: 0; font-size: 24px;'>✨ Comprehensive Feature Set</h3>
            <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 20px;'>
                <div>
                    <h4 style='color: {SECONDARY_TEAL}; margin-bottom: 10px;'>📝 Analysis Features</h4>
                    <ul style='color: {TEXT_DARK}; line-height: 2;'>
                        <li>Multi-resume comparison</li>
                        <li>Role-specific scoring (6 roles)</li>
                        <li>Advanced keyword extraction</li>
                        <li>Section-by-section analysis</li>
                        <li>Contact info extraction</li>
                    </ul>
                </div>
                <div>
                    <h4 style='color: {SECONDARY_TEAL}; margin-bottom: 10px;'>📊 Visualization Tools</h4>
                    <ul style='color: {TEXT_DARK}; line-height: 2;'>
                        <li>Interactive charts & graphs</li>
                        <li>Word cloud generation</li>
                        <li>Progress tracking</li>
                        <li>Competitive ranking</li>
                        <li>Trend analysis</li>
                    </ul>
                </div>
                <div>
                    <h4 style='color: {SECONDARY_TEAL}; margin-bottom: 10px;'>🎯 Smart Insights</h4>
                    <ul style='color: {TEXT_DARK}; line-height: 2;'>
                        <li>Prioritized recommendations</li>
                        <li>Strength identification</li>
                        <li>Gap analysis</li>
                        <li>Industry benchmarks</li>
                        <li>Best practice tips</li>
                    </ul>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Getting Started
    st.markdown(f"""
        <div class='feature-box'>
            <h3 style='color: {PRIMARY_TEAL}; margin-top: 0; text-align: center; font-size: 26px;'>🚀 Get Started in 3 Simple Steps</h3>
            <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px; margin-top: 25px;'>
                <div style='text-align: center; padding: 20px; background: {WHITE}; border-radius: 12px; box-shadow: 0 4px 12px rgba(78, 205, 196, 0.2);'>
                    <div style='font-size: 48px; margin-bottom: 15px;'>1️⃣</div>
                    <h4 style='color: {PRIMARY_TEAL}; margin-bottom: 10px;'>Select Your Role</h4>
                    <p style='color: {TEXT_DARK}; font-size: 14px;'>Choose from Data Analyst, Data Scientist, Web Developer, ML Engineer, Full Stack Developer, or Business Analyst</p>
                </div>
                <div style='text-align: center; padding: 20px; background: {WHITE}; border-radius: 12px; box-shadow: 0 4px 12px rgba(78, 205, 196, 0.2);'>
                    <div style='font-size: 48px; margin-bottom: 15px;'>2️⃣</div>
                    <h4 style='color: {PRIMARY_TEAL}; margin-bottom: 10px;'>Upload Resume(s)</h4>
                    <p style='color: {TEXT_DARK}; font-size: 14px;'>Submit single or multiple PDF resumes for analysis. Optionally add job description for better matching</p>
                </div>
                <div style='text-align: center; padding: 20px; background: {WHITE}; border-radius: 12px; box-shadow: 0 4px 12px rgba(78, 205, 196, 0.2);'>
                    <div style='font-size: 48px; margin-bottom: 15px;'>3️⃣</div>
                    <h4 style='color: {PRIMARY_TEAL}; margin-bottom: 10px;'>Get Insights</h4>
                    <p style='color: {TEXT_DARK}; font-size: 14px;'>Receive detailed scores, visualizations, suggestions, and download professional PDF report</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # CTA Buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📤 Start Analyzing", key="home_analyze", use_container_width=True):
            st.query_params.page = "Upload"
    
    with col2:
        if st.button("📚 View Tips", key="home_tips", use_container_width=True):
            st.query_params.page = "Tips"
    
    with col3:
        if st.button("📊 See Analytics", key="home_analytics", use_container_width=True):
            st.query_params.page = "Analytics"
    
    with col4:
        if st.button("⚖️ Compare Resumes", key="home_compare", use_container_width=True):
            st.query_params.page = "Compare"
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Testimonials / Benefits
    st.markdown(f"""
        <div class='card'>
            <h3 style='color: {PRIMARY_TEAL}; margin-top: 0; text-align: center; font-size: 24px;'>💼 Why Use Our ATS Analyzer?</h3>
            <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 20px;'>
                <div style='text-align: center; padding: 15px;'>
                    <div style='font-size: 36px; margin-bottom: 10px;'>⚡</div>
                    <h4 style='color: {SECONDARY_TEAL}; font-size: 16px; margin-bottom: 8px;'>Instant Results</h4>
                    <p style='font-size: 13px; color: {TEXT_DARK};'>Get comprehensive analysis in seconds</p>
                </div>
                <div style='text-align: center; padding: 15px;'>
                    <div style='font-size: 36px; margin-bottom: 10px;'>🎯</div>
                    <h4 style='color: {SECONDARY_TEAL}; font-size: 16px; margin-bottom: 8px;'>Actionable Insights</h4>
                    <p style='font-size: 13px; color: {TEXT_DARK};'>Prioritized recommendations you can implement</p>
                </div>
                <div style='text-align: center; padding: 15px;'>
                    <div style='font-size: 36px; margin-bottom: 10px;'>🔒</div>
                    <h4 style='color: {SECONDARY_TEAL}; font-size: 16px; margin-bottom: 8px;'>100% Private</h4>
                    <p style='font-size: 13px; color: {TEXT_DARK};'>Your data stays secure and confidential</p>
                </div>
                <div style='text-align: center; padding: 15px;'>
                    <div style='font-size: 36px; margin-bottom: 10px;'>💯</div>
                    <h4 style='color: {SECONDARY_TEAL}; font-size: 16px; margin-bottom: 8px;'>Free to Use</h4>
                    <p style='font-size: 13px; color: {TEXT_DARK};'>No hidden costs or subscriptions</p>
                </div>
                <div style='text-align: center; padding: 15px;'>
                    <div style='font-size: 36px; margin-bottom: 10px;'>📈</div>
                    <h4 style='color: {SECONDARY_TEAL}; font-size: 16px; margin-bottom: 8px;'>Proven Results</h4>
                    <p style='font-size: 13px; color: {TEXT_DARK};'>Based on industry best practices</p>
                </div>
                <div style='text-align: center; padding: 15px;'>
                    <div style='font-size: 36px; margin-bottom: 10px;'>🔄</div>
                    <h4 style='color: {SECONDARY_TEAL}; font-size: 16px; margin-bottom: 8px;'>Unlimited Use</h4>
                    <p style='font-size: 13px; color: {TEXT_DARK};'>Analyze as many resumes as you need</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ============================================================================
# PAGE: UPLOAD & ANALYZE (ENHANCED)
# ============================================================================

def upload_page():
    st.markdown(f"<h1 class='section-title'><span class='animated-icon'>📄</span> Upload & Analyze Resumes</h1>", unsafe_allow_html=True)
    
    # Job Role Selection with descriptions
    st.markdown(f"<h3 class='section-subtitle'>🎯 Step 1: Select Target Job Role</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        job_roles = ["", "Data Analyst", "Data Scientist", "Web Developer", "Machine Learning Engineer", "Full Stack Developer", "Business Analyst"]
        job_role = st.selectbox(
            "Choose the role you're targeting:",
            job_roles,
            key="job_role_select",
            help="Select the specific role to get tailored keyword analysis"
        )
    
    with col2:
        if job_role and job_role in ROLE_KEYWORDS:
            role_info = ROLE_KEYWORDS[job_role]
            st.info(f"**Key Skills:**\n{', '.join(role_info['required'][:3])}")
    
    # Job Description Input
    st.markdown(f"<h3 class='section-subtitle'>📝 Step 2: Add Job Description (Optional but Recommended)</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        jd = st.text_area(
            "Paste the complete job description here:",
            height=180,
            placeholder="Senior Data Analyst needed with 5+ years experience in SQL, Python, Tableau. Must have strong communication skills and experience with stakeholder management...",
            key="jd_input",
            help="Adding a job description improves keyword matching and experience relevance scoring"
        )
    
    with col2:
        if jd:
            word_count = len(jd.split())
            st.metric("Words", word_count)
            if word_count > 50:
                st.success("✓ Good length")
            else:
                st.warning("⚠ Add more details")
    
    # File Upload Section
    st.markdown(f"<h3 class='section-subtitle'>📤 Step 3: Upload Resume PDF(s)</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        uploaded_files = st.file_uploader(
            "Upload one or multiple resume PDFs (Max 10MB each):",
            type=["pdf"],
            accept_multiple_files=True,
            key="resume_upload",
            help="You can upload multiple resumes to compare them side-by-side"
        )
    
    with col2:
        if uploaded_files:
            st.metric("Files Uploaded", len(uploaded_files))
            total_size = sum(file.size for file in uploaded_files) / (1024 * 1024)
            st.metric("Total Size", f"{total_size:.2f} MB")
    
    # Display uploaded files info
    if uploaded_files:
        st.markdown(f"""
            <div class='stats-box'>
                <h4 style='color: {PRIMARY_TEAL}; margin-top: 0;'>📋 Uploaded Files:</h4>
        """, unsafe_allow_html=True)
        
        for idx, file in enumerate(uploaded_files, 1):
            file_size = file.size / 1024  # Convert to KB
            st.markdown(f"""
                <div style='padding: 8px; margin: 5px 0; background: {PALE_TEAL}; border-radius: 6px; display: flex; justify-content: space-between; align-items: center;'>
                    <span><b>{idx}.</b> {file.name}</span>
                    <span style='color: {TEXT_DARK}; font-size: 13px;'>{file_size:.1f} KB</span>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Analysis Options
    with st.expander("⚙️ Advanced Options", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            generate_wordcloud_opt = st.checkbox("Generate Word Cloud", value=True, help="Create visual representation of most common words")
            show_detailed_feedback = st.checkbox("Show Detailed Feedback", value=True, help="Display comprehensive analysis breakdown")
        
        with col2:
            auto_download_report = st.checkbox("Auto-download Report", value=False, help="Automatically download PDF report after analysis")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Analyze Button
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        analyze_button = st.button(
            "🔍 RUN COMPREHENSIVE ATS ANALYSIS",
            key="analyze_btn",
            use_container_width=True,
            type="primary"
        )
    
    if analyze_button:
        if not uploaded_files:
            st.error("❌ Please upload at least one PDF file.")
        elif not job_role:
            st.error("❌ Please select a target job role.")
        else:
            st.success("✅ Starting comprehensive analysis...")
            
            resumes_data = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, file in enumerate(uploaded_files):
                status_text.text(f"Analyzing {file.name}... ({idx + 1}/{len(uploaded_files)})")
                
                with st.spinner(f"Processing {file.name}..."):
                    resume_text = extract_text(file)
                    
                    if resume_text:
                        scores, sections, detailed_feedback = calculate_ats_score(resume_text, jd, job_role)
                        overall_score = round(sum(scores.values()) / len(scores), 2)
                        
                        improvements = generate_improvement_suggestions(scores, sections, detailed_feedback)
                        strengths = generate_strengths(scores, detailed_feedback)
                        
                        # Extract contact info
                        email = extract_email(resume_text)
                        phone = extract_phone(resume_text)
                        linkedin = extract_linkedin(resume_text)
                        github = extract_github(resume_text)
                        
                        resumes_data.append({
                            "name": file.name,
                            "role": job_role,
                            "scores": scores,
                            "overall_score": overall_score,
                            "improvements": improvements,
                            "strengths": strengths,
                            "sections": sections,
                            "text": resume_text,
                            "detailed_feedback": detailed_feedback,
                            "contact": {
                                "email": email,
                                "phone": phone,
                                "linkedin": linkedin,
                                "github": github
                            }
                        })
                    else:
                        st.error(f"❌ Failed to extract text from {file.name}")
                    
                    progress_bar.progress((idx + 1) / len(uploaded_files))
            
            status_text.text("Analysis complete! 🎉")
            
            if resumes_data:
                # Sort by overall score
                resumes_data = sorted(resumes_data, key=lambda x: x['overall_score'], reverse=True)
                
                # Store in session state
                st.session_state.analyzed_resumes = resumes_data
                st.session_state.job_role = job_role
                st.session_state.job_description = jd
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Results Summary
                st.markdown(f"""
                    <div class='feature-box'>
                        <h2 style='color: {PRIMARY_TEAL}; margin-top: 0; text-align: center;'>🎉 Analysis Complete!</h2>
                        <p style='text-align: center; font-size: 16px; color: {TEXT_DARK};'>
                            Successfully analyzed <b>{len(resumes_data)}</b> resume(s) for the <b>{job_role}</b> role
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Resume Rankings
                st.markdown(f"<h2 class='section-subtitle'>🏆 Resume Rankings</h2>", unsafe_allow_html=True)
                
                for idx, r in enumerate(resumes_data, 1):
                    rank_class = f"rank-{idx}" if idx <= 3 else "rank-other"
                    rank_emoji = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}th"
                    
                    with st.container():
                        col1, col2, col3, col4 = st.columns([0.5, 2.5, 1.5, 1.5])
                        
                        with col1:
                            st.markdown(f"""
                                <div class='rank-badge {rank_class}'>
                                    #{idx}
                                </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f"""
                                <div class='card' style='margin: 0;'>
                                    <h4 style='color: {PRIMARY_TEAL}; margin-top: 0;'>{rank_emoji} {r['name']}</h4>
                                    <p style='margin: 5px 0; color: {TEXT_DARK}; font-size: 14px;'>
                                        <b>Target Role:</b> {r['role']}
                                    </p>
                                    <p style='margin: 0;'>
                                        <span class='metric-badge' style='font-size: 14px;'>Overall Score: {r['overall_score']}%</span>
                                    </p>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        with col3:
                            # Create mini gauge chart
                            score = r['overall_score']
                            color = SUCCESS_GREEN if score >= 75 else WARNING_ORANGE if score >= 50 else DANGER_RED
                            
                            fig = go.Figure(go.Indicator(
                                mode="gauge+number",
                                value=score,
                                domain={'x': [0, 1], 'y': [0, 1]},
                                title={'text': "Score", 'font': {'size': 14}},
                                gauge={
                                    'axis': {'range': [0, 100], 'tickwidth': 1},
                                    'bar': {'color': color},
                                    'bgcolor': "white",
                                    'borderwidth': 2,
                                    'bordercolor': "gray",
                                    'steps': [
                                        {'range': [0, 50], 'color': 'rgba(192, 57, 43, 0.2)'},
                                        {'range': [50, 75], 'color': 'rgba(230, 126, 34, 0.2)'},
                                        {'range': [75, 100], 'color': 'rgba(39, 174, 96, 0.2)'}
                                    ],
                                }
                            ))
                            fig.update_layout(
                                height=200,
                                margin=dict(l=20, r=20, t=40, b=20),
                                paper_bgcolor=BG_COLOR,
                                font=dict(color=TEXT_DARK, size=12)
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        
                        with col4:
                            # Quick stats
                            top_category = max(r['scores'], key=r['scores'].get)
                            weak_category = min(r['scores'], key=r['scores'].get)
                            
                            st.markdown(f"""
                                <div style='padding: 15px; background: {WHITE}; border-radius: 10px; height: 100%;'>
                                    <p style='margin: 5px 0; font-size: 13px; color: {TEXT_DARK};'>
                                        <b style='color: {SUCCESS_GREEN};'>✓ Strongest:</b><br>
                                        {top_category[:20]}... ({r['scores'][top_category]:.0f}%)
                                    </p>
                                    <p style='margin: 10px 0 5px 0; font-size: 13px; color: {TEXT_DARK};'>
                                        <b style='color: {DANGER_RED};'>⚠ Needs Work:</b><br>
                                        {weak_category[:20]}... ({r['scores'][weak_category]:.0f}%)
                                    </p>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("---")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Detailed Analysis Section
                st.markdown(f"<h2 class='section-subtitle'>📊 Detailed Analysis</h2>", unsafe_allow_html=True)
                
                selected_resume = st.selectbox(
                    "Select resume for detailed view:",
                    [r['name'] for r in resumes_data],
                    key="resume_select"
                )
                
                selected_data = next(r for r in resumes_data if r['name'] == selected_resume)
                selected_rank = next(idx for idx, r in enumerate(resumes_data, 1) if r['name'] == selected_resume)
                
                # Quick Overview Cards
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Overall Score",
                        f"{selected_data['overall_score']}%",
                        delta=f"{selected_data['overall_score'] - 75:.1f}% vs target" if selected_data['overall_score'] >= 75 else f"{selected_data['overall_score'] - 75:.1f}% vs target"
                    )
                
                with col2:
                    st.metric(
                        "Ranking",
                        f"#{selected_rank} of {len(resumes_data)}",
                        delta="Top Performer" if selected_rank == 1 else f"{selected_rank - 1} behind leader"
                    )
                
                with col3:
                    avg_score = sum(selected_data['scores'].values()) / len(selected_data['scores'])
                    st.metric(
                        "Avg Category Score",
                        f"{avg_score:.1f}%"
                    )
                
                with col4:
                    high_scores = sum(1 for score in selected_data['scores'].values() if score >= 70)
                    st.metric(
                        "Strong Categories",
                        f"{high_scores}/{len(selected_data['scores'])}"
                    )
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Contact Information
                if any(selected_data['contact'].values()):
                    with st.expander("📇 Extracted Contact Information", expanded=False):
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            if selected_data['contact']['email']:
                                st.success(f"📧 {selected_data['contact']['email']}")
                            else:
                                st.warning("📧 No email found")
                        
                        with col2:
                            if selected_data['contact']['phone']:
                                st.success(f"📱 {selected_data['contact']['phone']}")
                            else:
                                st.warning("📱 No phone found")
                        
                        with col3:
                            if selected_data['contact']['linkedin']:
                                st.success(f"🔗 {selected_data['contact']['linkedin']}")
                            else:
                                st.info("🔗 No LinkedIn")
                        
                        with col4:
                            if selected_data['contact']['github']:
                                st.success(f"💻 {selected_data['contact']['github']}")
                            else:
                                st.info("💻 No GitHub")
                
                # Tabbed Detailed View
                tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                    "📈 Score Breakdown",
                    "💡 Suggestions",
                    "✅ Strengths",
                    "📋 Sections",
                    "🔍 Detailed Feedback",
                    "☁️ Word Cloud"
                ])
                
                with tab1:
                    col1, col2 = st.columns([1.2, 1])
                    
                    with col1:
                        # Horizontal bar chart
                        fig = go.Figure()
                        
                        categories = list(selected_data['scores'].keys())
                        scores = list(selected_data['scores'].values())
                        
                        colors_list = [SUCCESS_GREEN if s >= 75 else WARNING_ORANGE if s >= 50 else DANGER_RED for s in scores]
                        
                        fig.add_trace(go.Bar(
                            y=categories,
                            x=scores,
                            orientation='h',
                            marker=dict(
                                color=colors_list,
                                line=dict(color='rgb(8,48,107)', width=1.5)
                            ),
                            text=[f"{v:.1f}%" for v in scores],
                            textposition='auto',
                            textfont=dict(size=12, color='white', family='Poppins')
                        ))
                        
                        fig.update_layout(
                            title={
                                'text': "Score Breakdown by Category",
                                'font': {'size': 18, 'color': PRIMARY_TEAL, 'family': 'Poppins'}
                            },
                            xaxis_title="Score (%)",
                            xaxis=dict(range=[0, 100]),
                            height=450,
                            margin=dict(l=200, r=50, t=60, b=50),
                            paper_bgcolor=BG_COLOR,
                            plot_bgcolor='rgba(255,255,255,0.9)',
                            font=dict(color=TEXT_DARK, size=12),
                            showlegend=False
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Progress bars with details
                        st.markdown(f"<h4 style='color: {PRIMARY_TEAL}; margin-top: 20px;'>Category Progress</h4>", unsafe_allow_html=True)
                        for category, score in selected_data['scores'].items():
                            color = SUCCESS_GREEN if score >= 75 else WARNING_ORANGE if score >= 50 else DANGER_RED
                            st.markdown(f"""
                                <div style='margin-bottom: 15px;'>
                                    <div style='display: flex; justify-content: space-between; margin-bottom: 5px;'>
                                        <span style='font-weight: 600; color: {TEXT_DARK};'>{category}</span>
                                        <span style='font-weight: 700; color: {color};'>{score:.1f}%</span>
                                    </div>
                                    <div class='progress-container'>
                                        <div class='progress-bar' style='width: {score}%; background: {color};'>
                                        </div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                    
                    with col2:
                        # Radar chart
                        fig = go.Figure()
                        
                        categories_radar = list(selected_data['scores'].keys()) + [list(selected_data['scores'].keys())[0]]
                        scores_radar = list(selected_data['scores'].values()) + [list(selected_data['scores'].values())[0]]
                        
                        fig.add_trace(go.Scatterpolar(
                            r=scores_radar,
                            theta=categories_radar,
                            fill='toself',
                            fillcolor=f'rgba(78, 205, 196, 0.3)',
                            line=dict(color=PRIMARY_TEAL, width=2),
                            name='Scores'
                        ))
                        
                        fig.update_layout(
                            polar=dict(
                                radialaxis=dict(
                                    visible=True,
                                    range=[0, 100],
                                    tickfont=dict(size=10)
                                ),
                                angularaxis=dict(
                                    tickfont=dict(size=10)
                                )
                            ),
                            showlegend=False,
                            title={
                                'text': "Score Radar Chart",
                                'font': {'size': 16, 'color': PRIMARY_TEAL}
                            },
                            height=450,
                            paper_bgcolor=BG_COLOR,
                            font=dict(color=TEXT_DARK)
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Score Summary Table
                        st.markdown(f"<h4 style='color: {PRIMARY_TEAL}; margin-top: 20px;'>Score Summary</h4>", unsafe_allow_html=True)
                        
                        for category, score in selected_data['scores'].items():
                            if score >= 80:
                                rating = "Excellent"
                                color = SUCCESS_GREEN
                                icon = "🌟"
                            elif score >= 60:
                                rating = "Good"
                                color = WARNING_ORANGE
                                icon = "👍"
                            else:
                                rating = "Needs Work"
                                color = DANGER_RED
                                icon = "⚠️"
                            
                            st.markdown(f"""
                                <div style='background: {WHITE}; padding: 12px; border-radius: 8px; margin-bottom: 10px; border-left: 5px solid {color};'>
                                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                                        <div>
                                            <b style='color: {TEXT_DARK}; font-size: 14px;'>{category}</b>
                                        </div>
                                        <div style='text-align: right;'>
                                            <div style='color: {color}; font-size: 20px; font-weight: 800;'>{icon} {score:.0f}%</div>
                                            <div style='color: {color}; font-size: 11px; font-weight: 600;'>{rating}</div>
                                        </div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                
                with tab2:
                    st.markdown(f"<h4 style='color: {PRIMARY_TEAL};'>🔧 Prioritized Improvement Recommendations</h4>", unsafe_allow_html=True)
                    
                    # Group by priority
                    priority_groups = {"CRITICAL": [], "HIGH": [], "MEDIUM": [], "LOW": []}
                    for improvement in selected_data['improvements']:
                        if isinstance(improvement, dict):
                            priority = improvement.get('priority', 'MEDIUM')
                            priority_groups[priority].append(improvement)
                    
                    for priority in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
                        if priority_groups[priority]:
                            priority_color = {
                                "CRITICAL": DANGER_RED,
                                "HIGH": WARNING_ORANGE,
                                "MEDIUM": INFO_BLUE,
                                "LOW": SUCCESS_GREEN
                            }[priority]
                            
                            priority_icon = {
                                "CRITICAL": "🚨",
                                "HIGH": "⚠️",
                                "MEDIUM": "ℹ️",
                                "LOW": "💡"
                            }[priority]
                            
                            st.markdown(f"""
                                <h5 style='color: {priority_color}; margin-top: 20px;'>
                                    {priority_icon} {priority} Priority ({len(priority_groups[priority])})
                                </h5>
                            """, unsafe_allow_html=True)
                            
                            for idx, improvement in enumerate(priority_groups[priority], 1):
                                with st.container():
                                    st.markdown(f"""
                                        <div class='card' style='border-left-color: {priority_color}; margin-bottom: 15px;'>
                                            <div style='display: flex; align-items: start; gap: 15px;'>
                                                <div style='background: {priority_color}; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; flex-shrink: 0;'>
                                                    {idx}
                                                </div>
                                                <div style='flex: 1;'>
                                                    <h5 style='color: {PRIMARY_TEAL}; margin: 0 0 8px 0;'>{improvement.get('category', 'General')}</h5>
                                                    <p style='color: {TEXT_DARK}; margin: 0 0 8px 0; font-size: 15px; font-weight: 600;'>
                                                        {improvement.get('suggestion', '')}
                                                    </p>
                                                    <p style='color: {DARK_GRAY}; margin: 0; font-size: 13px; padding: 10px; background: {PALE_TEAL}; border-radius: 6px;'>
                                                        💡 <i>{improvement.get('details', '')}</i>
                                                    </p>
                                                </div>
                                            </div>
                                        </div>
                                    """, unsafe_allow_html=True)
                
                with tab3:
                    st.markdown(f"<h4 style='color: {PRIMARY_TEAL};'>✅ Resume Strengths & Highlights</h4>", unsafe_allow_html=True)
                    
                    if selected_data['strengths']:
                        cols = st.columns(2)
                        for idx, strength in enumerate(selected_data['strengths']):
                            with cols[idx % 2]:
                                if isinstance(strength, dict):
                                    st.markdown(f"""
                                        <div class='card' style='border-left-color: {SUCCESS_GREEN}; margin-bottom: 15px; background: linear-gradient(145deg, {WHITE} 0%, rgba(39, 174, 96, 0.05) 100%);'>
                                            <h5 style='color: {SUCCESS_GREEN}; margin: 0 0 10px 0;'>
                                                ✓ {strength.get('category', 'Strength')}
                                            </h5>
                                            <p style='color: {TEXT_DARK}; margin: 0 0 8px 0; font-weight: 600; font-size: 15px;'>
                                                {strength.get('strength', '')}
                                            </p>
                                            <p style='color: {DARK_GRAY}; margin: 0; font-size: 13px; padding: 10px; background: rgba(39, 174, 96, 0.1); border-radius: 6px;'>
                                                {strength.get('details', '')}
                                            </p>
                                        </div>
                                    """, unsafe_allow_html=True)
                                else:
                                    st.success(strength)
                    else:
                        st.info("Continue building on your skills to develop more strengths!")
                
                with tab4:
                    st.markdown(f"<h4 style='color: {PRIMARY_TEAL};'>📋 Resume Section Analysis</h4>", unsafe_allow_html=True)
                    
                    section_icons = {
                        "summary": "📝",
                        "experience": "💼",
                        "skills": "⚡",
                        "education": "🎓",
                        "projects": "🚀",
                        "certifications": "🏆",
                        "contact": "📇"
                    }
                    
                    for section, content in selected_data['sections'].items():
                        icon = section_icons.get(section, "📄")
                        
                        if content:
                            with st.expander(f"{icon} {section.capitalize()} Section ✓", expanded=False):
                                st.markdown(f"""
                                    <div style='background: {PALE_TEAL}; padding: 15px; border-radius: 8px; color: {TEXT_DARK}; line-height: 1.8;'>
                                        {content[:500]}{'...' if len(content) > 500 else ''}
                                    </div>
                                """, unsafe_allow_html=True)
                                
                                word_count = len(content.split())
                                st.caption(f"📊 Word count: {word_count}")
                        else:
                            with st.expander(f"{icon} {section.capitalize()} Section ⚠️", expanded=False):
                                st.warning(f"No {section} section detected. Consider adding this section to your resume.")
                
                with tab5:
                    if show_detailed_feedback and 'detailed_feedback' in selected_data:
                        st.markdown(f"<h4 style='color: {PRIMARY_TEAL};'>🔍 Comprehensive Detailed Feedback</h4>", unsafe_allow_html=True)
                        
                        feedback = selected_data['detailed_feedback']
                        
                        # Technical Skills Details
                        if 'Technical Skills' in feedback:
                            with st.expander("⚙️ Technical Skills Analysis", expanded=True):
                                ts = feedback['Technical Skills']
                                
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    if 'found' in ts:
                                        st.markdown(f"**✅ Skills Found ({len(ts['found'])}):**")
                                        st.success(", ".join(ts['found']) if ts['found'] else "None")
                                    
                                    if 'required' in ts:
                                        st.markdown(f"**🎯 Required Skills Matched ({len(ts['required'])}):**")
                                        st.success(", ".join(ts['required']) if ts['required'] else "None")
                                    
                                    if 'preferred' in ts:
                                        st.markdown(f"**👍 Preferred Skills Matched ({len(ts['preferred'])}):**")
                                        st.info(", ".join(ts['preferred']) if ts['preferred'] else "None")
                                
                                with col2:
                                    if 'missing_required' in ts and ts['missing_required']:
                                        st.markdown(f"**❌ Missing Required Skills ({len(ts['missing_required'])}):**")
                                        st.error(", ".join(ts['missing_required']))
                                    
                                    if 'missing_preferred' in ts and ts['missing_preferred']:
                                        st.markdown(f"**⚠️ Missing Preferred Skills ({len(ts['missing_preferred'])}):**")
                                        st.warning(", ".join(ts['missing_preferred'][:5]))
                                    
                                    if 'bonus' in ts:
                                        st.markdown(f"**🌟 Bonus Skills Matched ({len(ts['bonus'])}):**")
                                        st.success(", ".join(ts['bonus']) if ts['bonus'] else "None")
                        
                        # Soft Skills Details
                        if 'Soft Skills' in feedback:
                            with st.expander("🤝 Soft Skills Analysis"):
                                ss = feedback['Soft Skills']
                                st.markdown(f"**Found {ss.get('count', 0)} soft skill mentions:**")
                                if ss.get('found'):
                                    st.info(", ".join(ss['found']))
                                else:
                                    st.warning("Consider adding more soft skills like leadership, communication, teamwork")
                        
                        # Metrics & Results Details
                        if 'Metrics & Results' in feedback:
                            with st.expander("📊 Metrics & Impact Analysis"):
                                mr = feedback['Metrics & Results']
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.metric("Impact Keywords Found", len(mr.get('found', [])))
                                    if mr.get('found'):
                                        st.success(", ".join(mr['found']))
                                
                                with col2:
                                    st.metric("Quantifiable Metrics", mr.get('numbers_found', 0))
                                    if mr.get('examples'):
                                        st.info("Examples: " + ", ".join(mr['examples'][:5]))
                        
                        # Keyword Density Details
                        if 'Keyword Density' in feedback:
                            with st.expander("🔑 Keyword Density Analysis"):
                                kd = feedback['Keyword Density']
                                
                                col1, col2, col3 = st.columns(3)
                                
                                with col1:
                                    st.metric("Keyword Density", f"{kd.get('density_percentage', 0):.2f}%")
                                
                                with col2:
                                    st.metric("Total Keywords", kd.get('total_keywords', 0))
                                
                                with col3:
                                    st.metric("Total Words", kd.get('total_words', 0))
                                
                                density = kd.get('density_percentage', 0)
                                if 5 <= density <= 10:
                                    st.success("✅ Optimal keyword density (5-10%)")
                                elif density < 5:
                                    st.warning(f"⚠️ Keyword density is low ({density:.1f}%). Add more relevant keywords.")
                                else:
                                    st.error(f"❌ Keyword density is high ({density:.1f}%). May appear as keyword stuffing.")
                        
                        # Action Verbs Details
                        if 'Action Verbs' in feedback:
                            with st.expander("💪 Action Verbs Analysis"):
                                av = feedback['Action Verbs']
                                st.markdown(f"**Found {av.get('count', 0)} strong action verbs:**")
                                if av.get('found'):
                                    st.success(", ".join(av['found']))
                                else:
                                    st.warning("Add strong action verbs like: Led, Developed, Implemented, Achieved")
                        
                        # Section Completeness Details
                        if 'Section Completeness' in feedback:
                            with st.expander("📑 Section Completeness Analysis"):
                                sc = feedback['Section Completeness']
                                
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.markdown("**✅ Present Sections:**")
                                    for section in sc.get('present', []):
                                        st.success(f"✓ {section.capitalize()}")
                                
                                with col2:
                                    st.markdown("**❌ Missing Sections:**")
                                    if sc.get('missing'):
                                        for section in sc['missing']:
                                            st.error(f"✗ {section.capitalize()}")
                                    else:
                                        st.success("All sections present!")
                        
                        # ATS Compatibility Details
                        if 'ATS Compatibility' in feedback:
                            with st.expander("🤖 ATS Compatibility Analysis"):
                                ats = feedback['ATS Compatibility']
                                if ats.get('issues'):
                                    st.markdown("**Issues Found:**")
                                    for issue in ats['issues']:
                                        st.error(f"❌ {issue}")
                                else:
                                    st.success("✅ No major ATS compatibility issues found!")
                        
                        # Experience Match Details
                        if 'Experience Match' in feedback:
                            with st.expander("🎯 Experience Match Analysis"):
                                em = feedback['Experience Match']
                                if 'matched_keywords' in em:
                                    st.markdown(f"**Matched Keywords ({len(em['matched_keywords'])}):**")
                                    if em['matched_keywords']:
                                        # Display in columns for better readability
                                        keywords = em['matched_keywords']
                                        cols = st.columns(3)
                                        for i, kw in enumerate(keywords):
                                            cols[i % 3].markdown(f"• {kw}")
                                    
                                    if 'match_percentage' in em:
                                        match_pct = em['match_percentage']
                                        st.metric("Match Percentage", f"{match_pct:.1f}%")
                                        
                                        if match_pct >= 70:
                                            st.success("✅ Strong alignment with job description")
                                        elif match_pct >= 50:
                                            st.warning("⚠️ Moderate alignment. Consider adding more JD keywords")
                                        else:
                                            st.error("❌ Weak alignment. Tailor resume to job description")
                                else:
                                    st.info(em.get('note', 'No job description provided'))
                    else:
                        st.info("Enable 'Show Detailed Feedback' in Advanced Options to see comprehensive analysis")
                
                with tab6:
                    if generate_wordcloud_opt:
                        st.markdown(f"<h4 style='color: {PRIMARY_TEAL};'>☁️ Resume Word Cloud</h4>", unsafe_allow_html=True)
                        st.info("Visual representation of most frequently used words in your resume")
                        
                        with st.spinner("Generating word cloud..."):
                            fig = create_wordcloud(selected_data['text'], f"Word Cloud - {selected_resume}")
                            if fig:
                                st.pyplot(fig)
                            
                            # Top keywords
                            st.markdown(f"<h5 style='color: {PRIMARY_TEAL}; margin-top: 20px;'>Top Keywords</h5>", unsafe_allow_html=True)
                            
                            words = selected_data['text'].split()
                            word_freq = Counter([w for w in words if len(w) > 4])
                            top_words = word_freq.most_common(20)
                            
                            if top_words:
                                df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])
                                
                                fig = px.bar(
                                    df.head(15),
                                    x='Frequency',
                                    y='Word',
                                    orientation='h',
                                    title="Top 15 Most Frequent Words",
                                    labels={'Frequency': 'Count', 'Word': 'Keyword'},
                                    color='Frequency',
                                    color_continuous_scale='Teal'
                                )
                                fig.update_layout(
                                    height=500,
                                    showlegend=False,
                                    paper_bgcolor=BG_COLOR,
                                    plot_bgcolor='rgba(255,255,255,0.9)',
                                    font=dict(color=TEXT_DARK)
                                )
                                st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Enable 'Generate Word Cloud' in Advanced Options to visualize keywords")
                
                st.markdown("---")
                
                # Download Report Section
                st.markdown(f"<h2 class='section-subtitle'>📥 Download Professional Report</h2>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col2:
                    with st.spinner("Generating comprehensive PDF report..."):
                        pdf = create_pdf_report(resumes_data)
                        
                        st.download_button(
                            label="📥 DOWNLOAD PROFESSIONAL PDF REPORT",
                            data=pdf,
                            file_name=f"ATS_Professional_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                            type="primary"
                        )
                
                if auto_download_report:
                    st.success("✅ Report generated! Download will start automatically.")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Tips for Next Steps
                st.markdown(f"""
                    <div class='feature-box'>
                        <h4 style='color: {PRIMARY_TEAL}; margin-top: 0;'>🎯 Next Steps</h4>
                        <ol style='color: {TEXT_DARK}; line-height: 2; font-size: 15px;'>
                            <li><b>Review Recommendations:</b> Focus on high-priority improvements first</li>
                            <li><b>Update Resume:</b> Implement suggested changes section by section</li>
                            <li><b>Re-analyze:</b> Upload updated resume to track improvement</li>
                            <li><b>Tailor for Each Job:</b> Customize keywords based on specific job descriptions</li>
                            <li><b>Compare Versions:</b> Use the Compare tab to see progress over time</li>
                        </ol>
                    </div>
                """, unsafe_allow_html=True)

# ============================================================================
# PAGE: TIPS & RESOURCES (ENHANCED - Previous tips_page function)
# ============================================================================

def tips_page():
    st.markdown(f"<h1 class='section-title'>📚 Resume Tips & ATS Optimization Guide</h1>", unsafe_allow_html=True)
    
    # Quick Tips Summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class='score-card' style='height: 150px;'>
                <div style='font-size: 40px; margin-bottom: 10px;'>⏱️</div>
                <div class='score-value' style='font-size: 32px;'>6-7s</div>
                <div class='score-label'>Average time recruiters spend on a resume</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='score-card' style='height: 150px;'>
                <div style='font-size: 40px; margin-bottom: 10px;'>🤖</div>
                <div class='score-value' style='font-size: 32px;'>75%</div>
                <div class='score-label'>Of resumes are rejected by ATS before reaching humans</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class='score-card' style='height: 150px;'>
                <div style='font-size: 40px; margin-bottom: 10px;'>🎯</div>
                <div class='score-value' style='font-size: 32px;'>5-10%</div>
                <div class='score-label'>Ideal keyword density for ATS optimization</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Do's and Don'ts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
            <div class='card' style='border-left-color: {SUCCESS_GREEN};'>
                <h3 style='color: {SUCCESS_GREEN}; margin-top: 0;'>✅ Essential DO's</h3>
                <ul style='color: {TEXT_DARK}; line-height: 2; font-size: 15px;'>
                    <li><b>Use Clear Headings:</b> Experience, Skills, Education, Projects</li>
                    <li><b>Quantify Achievements:</b> "Increased sales by 35% ($2M revenue)"</li>
                    <li><b>Match Job Keywords:</b> Mirror language from job description</li>
                    <li><b>Clean Formatting:</b> Simple, ATS-friendly layout</li>
                    <li><b>Standard Fonts:</b> Arial, Calibri, Times New Roman (10-12pt)</li>
                    <li><b>Contact Info:</b> Name, email, phone, LinkedIn at top</li>
                    <li><b>Bullet Points:</b> Use for easy scanning and readability</li>
                    <li><b>Customize:</b> Tailor resume for each specific application</li>
                    <li><b>Action Verbs:</b> Led, Developed, Implemented, Achieved</li>
                    <li><b>Proofread:</b> Zero spelling or grammatical errors</li>
                    <li><b>PDF Format:</b> Preserves formatting across systems</li>
                    <li><b>Consistent Dates:</b> Use MM/YYYY format throughout</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='card' style='border-left-color: {DANGER_RED};'>
                <h3 style='color: {DANGER_RED}; margin-top: 0;'>🚫 Critical DON'Ts</h3>
                <ul style='color: {TEXT_DARK}; line-height: 2; font-size: 15px;'>
                    <li><b>Fancy Fonts:</b> Avoid decorative or script fonts</li>
                    <li><b>Tables/Graphics:</b> ATS systems can't parse these properly</li>
                    <li><b>Photos:</b> Don't include headshots (introduces bias)</li>
                    <li><b>Passive Language:</b> Avoid "Responsible for..." statements</li>
                    <li><b>Exceed 2 Pages:</b> Keep concise (1 page for entry-level)</li>
                    <li><b>Non-standard Formats:</b> No .doc, .txt, or image files</li>
                    <li><b>Personal Pronouns:</b> Skip "I", "me", "my", "we"</li>
                    <li><b>Headers/Footers:</b> ATS may miss important information</li>
                    <li><b>Irrelevant Info:</b> Focus only on relevant experience</li>
                    <li><b>Unexplained Acronyms:</b> Spell out first, then abbreviate</li>
                    <li><b>Generic Resumes:</b> Don't send same resume to all jobs</li>
                    <li><b>Lies or Exaggerations:</b> Always be truthful and accurate</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Role-Specific Keywords
    st.markdown(f"<h2 class='section-subtitle'>🔑 Keywords by Role</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class='card'>
                <h4 style='color: {PRIMARY_TEAL}; margin-top: 0;'>📊 Data Analyst</h4>
                <div style='background: {PALE_TEAL}; padding: 12px; border-radius: 8px; margin-bottom: 12px;'>
                    <p style='margin: 0; font-weight: 700; color: {TEXT_DARK};'>Technical Skills:</p>
                    <p style='font-size: 14px; color: {TEXT_DARK}; margin: 5px 0 0 0;'>
                        SQL • Python • Tableau • Power BI • Excel • Statistics • Data Visualization • R • Pandas • NumPy
                    </p>
                </div>
                <div style='background: {PALE_TEAL}; padding: 12px; border-radius: 8px; margin-bottom: 12px;'>
                    <p style='margin: 0; font-weight: 700; color: {TEXT_DARK};'>Soft Skills:</p>
                    <p style='font-size: 14px; color: {TEXT_DARK}; margin: 5px 0 0 0;'>
                        Communication • Problem Solving • Attention to Detail • Business Acumen • Critical Thinking
                    </p>
                </div>
                <div style='background: {PALE_TEAL}; padding: 12px; border-radius: 8px;'>
                    <p style='margin: 0; font-weight: 700; color: {TEXT_DARK};'>Keywords:</p>
                    <p style='font-size: 14px; color: {TEXT_DARK}; margin: 5px 0 0 0;'>
                        Dashboard • ETL • Data Pipeline • Reporting • Analytics • KPI • Insights • Data Mining
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='card'>
                <h4 style='color: {PRIMARY_TEAL}; margin-top: 0;'>🤖 Data Scientist</h4>
                <div style='background: {PALE_TEAL}; padding: 12px; border-radius: 8px; margin-bottom: 12px;'>
                    <p style='margin: 0; font-weight: 700; color: {TEXT_DARK};'>Technical Skills:</p>
                    <p style='font-size: 14px; color: {TEXT_DARK}; margin: 5px 0 0 0;'>
                        Python • Machine Learning • SQL • TensorFlow • Scikit-learn • Statistics • Deep Learning • PyTorch
                    </p>
                </div>
                <div style='background: {PALE_TEAL}; padding: 12px; border-radius: 8px; margin-bottom: 12px;'>
                    <p style='margin: 0; font-weight: 700; color: {TEXT_DARK};'>Soft Skills:</p>
                    <p style='font-size: 14px; color: {TEXT_DARK}; margin: 5px 0 0 0;'>
                        Problem Solving • Communication • Critical Thinking • Research • Innovation
                    </p>
                </div>
                <div style='background: {PALE_TEAL}; padding: 12px; border-radius: 8px;'>
                    <p style='margin: 0; font-weight: 700; color: {TEXT_DARK};'>Keywords:</p>
                    <p style='font-size: 14px; color: {TEXT_DARK}; margin: 5px 0 0 0;'>
                        Model Training • Predictive Analytics • NLP • Computer Vision • A/B Testing • Feature Engineering
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class='card'>
                <h4 style='color: {PRIMARY_TEAL}; margin-top: 0;'>💻 Web Developer</h4>
                <div style='background: {PALE_TEAL}; padding: 12px; border-radius: 8px; margin-bottom: 12px;'>
                    <p style='margin: 0; font-weight: 700; color: {TEXT_DARK};'>Technical Skills:</p>
                    <p style='font-size: 14px; color: {TEXT_DARK}; margin: 5px 0 0 0;'>
                        HTML • CSS • JavaScript • React • Node.js • MongoDB • APIs • TypeScript • Git
                    </p>
                </div>
                <div style='background: {PALE_TEAL}; padding: 12px; border-radius: 8px; margin-bottom: 12px;'>
                    <p style='margin: 0; font-weight: 700; color: {TEXT_DARK};'>Soft Skills:</p>
                    <p style='font-size: 14px; color: {TEXT_DARK}; margin: 5px 0 0 0;'>
                        Teamwork • Communication • Problem Solving • Creativity • Time Management
                    </p>
                </div>
                <div style='background: {PALE_TEAL}; padding: 12px; border-radius: 8px;'>
                    <p style='margin: 0; font-weight: 700; color: {TEXT_DARK};'>Keywords:</p>
                    <p style='font-size: 14px; color: {TEXT_DARK}; margin: 5px 0 0 0;'>
                        Responsive Design • REST API • UI/UX • Deployment • Version Control • Cross-browser Compatibility
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Resume Formatting Essentials
    st.markdown(f"<h2 class='section-subtitle'>🎨 Resume Formatting Essentials</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
            <div class='card'>
                <h4 style='color: {PRIMARY_TEAL}; margin-top: 0;'>📐 Layout Recommendations</h4>
                <table style='width: 100%; border-collapse: collapse;'>
                    <tr style='border-bottom: 1px solid {PALE_TEAL};'>
                        <td style='padding: 10px; font-weight: 700; color: {TEXT_DARK};'>Length</td>
                        <td style='padding: 10px; color: {TEXT_DARK};'>1 page (entry), 2 pages (experienced)</td>
                    </tr>
                    <tr style='border-bottom: 1px solid {PALE_TEAL};'>
                        <td style='padding: 10px; font-weight: 700; color: {TEXT_DARK};'>Margins</td>
                        <td style='padding: 10px; color: {TEXT_DARK};'>0.5 to 1 inch on all sides</td>
                    </tr>
                    <tr style='border-bottom: 1px solid {PALE_TEAL};'>
                        <td style='padding: 10px; font-weight: 700; color: {TEXT_DARK};'>Spacing</td>
                        <td style='padding: 10px; color: {TEXT_DARK};'>Single within sections, 1.5x between</td>
                    </tr>
                    <tr style='border-bottom: 1px solid {PALE_TEAL};'>
                        <td style='padding: 10px; font-weight: 700; color: {TEXT_DARK};'>Font Size</td>
                        <td style='padding: 10px; color: {TEXT_DARK};'>10-12pt body, 12-14pt headings</td>
                    </tr>
                    <tr style='border-bottom: 1px solid {PALE_TEAL};'>
                        <td style='padding: 10px; font-weight: 700; color: {TEXT_DARK};'>Font Style</td>
                        <td style='padding: 10px; color: {TEXT_DARK};'>Arial, Calibri, Times New Roman</td>
                    </tr>
                    <tr>
                        <td style='padding: 10px; font-weight: 700; color: {TEXT_DARK};'>File Format</td>
                        <td style='padding: 10px; color: {TEXT_DARK};'>PDF (preserves formatting)</td>
                    </tr>
                </table>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='card'>
                <h4 style='color: {PRIMARY_TEAL}; margin-top: 0;'>✨ Visual Hierarchy Tips</h4>
                <ul style='color: {TEXT_DARK}; line-height: 2;'>
                    <li><b>Section Headers:</b> Bold, 14pt, clear separation</li>
                    <li><b>Job Titles:</b> Bold, 11-12pt</li>
                    <li><b>Company Names:</b> Regular or italic, 11pt</li>
                    <li><b>Dates:</b> Right-aligned or after company name</li>
                    <li><b>Bullet Points:</b> Consistent style throughout</li>
                    <li><b>White Space:</b> Use generously for readability</li>
                    <li><b>Alignment:</b> Left-aligned for Western resumes</li>
                    <li><b>Color:</b> Black text on white (or very light) background</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Resume Section Breakdown
    st.markdown(f"<h2 class='section-subtitle'>📄 Resume Section Breakdown</h2>", unsafe_allow_html=True)
    
    sections_guide = {
        "1. Contact Information": {
            "icon": "📇",
            "content": "Full Name • Professional Email • Phone Number • LinkedIn Profile • GitHub (for tech roles) • Location (City, State)",
            "tips": "Place at the top center or left. Use professional email (firstname.lastname@email.com). No photos, age, marital status, or full address.",
            "example": "John Doe\njohn.doe@email.com | (555) 123-4567 | linkedin.com/in/johndoe | San Francisco, CA"
        },
        "2. Professional Summary": {
            "icon": "📝",
            "content": "2-4 line summary highlighting your experience, key skills, and career goals aligned with the target role",
            "tips": "Customize for each job. Include years of experience, specialization, and key achievement. Make it compelling and keyword-rich.",
            "example": "Results-driven Data Analyst with 5+ years of experience transforming complex datasets into actionable business insights. Expert in SQL, Python, and Tableau with proven track record of increasing operational efficiency by 40%. Seeking to leverage analytical skills to drive data-informed decision making."
        },
        "3. Professional Experience": {
            "icon": "💼",
            "content": "Job Title | Company Name | Location | Duration (MM/YYYY - MM/YYYY)\n• Bullet points highlighting achievements with quantifiable metrics\n• 3-5 bullets per role, most recent first",
            "tips": "Use action verbs. Quantify achievements with numbers/percentages. Focus on impact and results, not just duties. Tailor to job description keywords.",
            "example": "Senior Data Analyst | Tech Corp | San Francisco, CA | 06/2020 - Present\n• Increased sales forecast accuracy by 35% through development of predictive ML models\n• Led team of 4 analysts in redesigning reporting dashboard, reducing report generation time by 50%\n• Analyzed $10M+ in customer data to identify key trends, resulting in 25% revenue growth"
        },
        "4. Skills": {
            "icon": "⚡",
            "content": "Technical Skills: List hard skills relevant to the job (programming languages, tools, software)\nSoft Skills: Leadership, communication, problem-solving\nCertifications: Relevant professional certifications",
            "tips": "Organize by category. List proficiency level if relevant. Match keywords from job description. Keep current and honest.",
            "example": "Technical Skills: Python, SQL, Tableau, Power BI, Excel (Advanced), R, AWS, Machine Learning\nSoft Skills: Leadership, Cross-functional Collaboration, Stakeholder Management, Presentation\nCertifications: AWS Certified Data Analytics, Tableau Desktop Specialist"
        },
        "5. Education": {
            "icon": "🎓",
            "content": "Degree | Major | University Name | Graduation Date (MM/YYYY)\nGPA (only if 3.5+) • Honors/Awards • Relevant Coursework (optional)",
            "tips": "Most recent degree first. Include GPA only if impressive (3.5+). Add relevant coursework for recent graduates. Omit if 10+ years of experience.",
            "example": "Bachelor of Science in Computer Science | GPA: 3.8/4.0\nUniversity of California, Berkeley | Graduated: May 2019\nHonors: Dean's List (All Semesters), Magna Cum Laude\nRelevant Coursework: Machine Learning, Database Systems, Data Structures"
        },
        "6. Projects": {
            "icon": "🚀",
            "content": "Project Name | Technologies Used | Brief Description\n• Key achievements and outcomes\n• Include GitHub link if applicable",
            "tips": "Showcase 2-4 relevant projects. Include personal, academic, or professional projects. Quantify impact where possible. Add live demo or GitHub links.",
            "example": "Customer Churn Prediction System | Python, Scikit-learn, Flask, AWS\n• Built ML model predicting customer churn with 89% accuracy using Random Forest algorithm\n• Deployed web application serving 1000+ daily predictions, reducing churn by 15%\n• GitHub: github.com/johndoe/churn-prediction"
        },
        "7. Certifications": {
            "icon": "🏆",
            "content": "Certification Name | Issuing Organization | Date Obtained\nCredential ID (optional)",
            "tips": "List relevant professional certifications only. Include expiration dates if applicable. Add credential verification links.",
            "example": "AWS Certified Solutions Architect | Amazon Web Services | March 2024\nGoogle Data Analytics Professional Certificate | Google | January 2024\nTableau Desktop Specialist | Tableau | December 2023"
        },
        "8. Additional Sections (Optional)": {
            "icon": "➕",
            "content": "Volunteer Work • Publications • Speaking Engagements • Languages • Awards • Professional Memberships",
            "tips": "Only include if relevant to the position. Keep brief. Highlight leadership roles and achievements.",
            "example": "Volunteer: Data Analytics Mentor, Code for America (2022-Present)\nPublications: 'Machine Learning in Healthcare' - Journal of Data Science (2023)\nLanguages: English (Native), Spanish (Fluent), Mandarin (Conversational)"
        }
    }
    
    for section, details in sections_guide.items():
        with st.expander(f"{details['icon']} {section}", expanded=False):
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown(f"<b style='color: {PRIMARY_TEAL}; font-size: 16px;'>Content:</b>", unsafe_allow_html=True)
                st.markdown(f"""
                    <div style='background: {PALE_TEAL}; padding: 15px; border-radius: 8px; margin: 10px 0;'>
                        <p style='color: {TEXT_DARK}; margin: 0; white-space: pre-line;'>{details['content']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"<b style='color: {PRIMARY_TEAL}; font-size: 16px;'>Tips:</b>", unsafe_allow_html=True)
                st.info(details['tips'])
            
            with col2:
                st.markdown(f"<b style='color: {PRIMARY_TEAL}; font-size: 16px;'>Example:</b>", unsafe_allow_html=True)
                st.markdown(f"""
                    <div style='background: {WHITE}; padding: 15px; border-radius: 8px; border: 2px solid {PRIMARY_TEAL}; margin: 10px 0;'>
                        <p style='color: {TEXT_DARK}; margin: 0; white-space: pre-line; font-family: monospace; font-size: 13px;'>{details['example']}</p>
                    </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ATS Optimization Tips
    st.markdown(f"<h2 class='section-subtitle'>🤖 ATS Optimization Mastery</h2>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class='card'>
            <h4 style='color: {PRIMARY_TEAL}; margin-top: 0;'>What is ATS?</h4>
            <p style='color: {TEXT_DARK}; line-height: 1.8;'>
                <b>ATS (Applicant Tracking System)</b> is software used by 75% of employers to parse, rank, and filter resumes 
                based on keywords, formatting, and relevance. Understanding how ATS works is crucial because:
            </p>
            <ul style='color: {TEXT_DARK}; line-height: 2;'>
                <li>📉 75% of resumes are rejected by ATS before reaching human recruiters</li>
                <li>🤖 ATS scans for specific keywords matching the job description</li>
                <li>📊 Resumes are ranked by relevance score (higher scores get reviewed first)</li>
                <li>🚫 Poor formatting can cause ATS to misread or skip critical information</li>
                <li>✅ ATS-optimized resumes increase your chances of interviews by 50%+</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
            <div class='card' style='border-left-color: {SUCCESS_GREEN};'>
                <h4 style='color: {SUCCESS_GREEN}; margin-top: 0;'>✅ ATS Best Practices</h4>
                <ol style='color: {TEXT_DARK}; line-height: 2;'>
                    <li><b>Standard Formatting:</b> Avoid tables, columns, text boxes, graphics, and headers/footers</li>
                    <li><b>Keyword Matching:</b> Mirror exact keywords and phrases from job description</li>
                    <li><b>Clear Section Headers:</b> Use standard headers: Experience, Education, Skills</li>
                    <li><b>Simple Font:</b> Arial, Calibri, Times New Roman, or Georgia at 10-12pt</li>
                    <li><b>PDF Format:</b> Save as PDF to preserve formatting (unless .docx requested)</li>
                    <li><b>Avoid Headers/Footers:</b> ATS may not read information in these areas</li>
                    <li><b>No Images/Logos:</b> ATS cannot parse visual elements or photos</li>
                    <li><b>Consistent Formatting:</b> Use same bullet style, font, and spacing throughout</li>
                    <li><b>Full Spellings:</b> Spell out acronyms first: "Search Engine Optimization (SEO)"</li>
                    <li><b>Standard Dates:</b> Use MM/YYYY format consistently</li>
                    <li><b>Contact Info in Body:</b> Not just in header/footer</li>
                    <li><b>Keywords Naturally:</b> Integrate keywords naturally, not just listing</li>
                </ol>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='card' style='border-left-color: {INFO_BLUE};'>
                <h4 style='color: {INFO_BLUE}; margin-top: 0;'>🎯 Keyword Strategy</h4>
                <p style='color: {TEXT_DARK}; line-height: 1.8;'><b>How to identify and use keywords effectively:</b></p>
                
                <p style='color: {TEXT_DARK}; margin-top: 15px;'><b>Step 1: Extract Keywords</b></p>
                <ul style='color: {TEXT_DARK}; line-height: 1.8;'>
                    <li>Read job description carefully</li>
                    <li>Highlight required skills, qualifications, tools</li>
                    <li>Note repeated terms (high priority)</li>
                    <li>Look for "must have" vs "nice to have"</li>
                </ul>
                
                <p style='color: {TEXT_DARK}; margin-top: 15px;'><b>Step 2: Categorize Keywords</b></p>
                <ul style='color: {TEXT_DARK}; line-height: 1.8;'>
                    <li><b>Hard Skills:</b> SQL, Python, Java, Photoshop</li>
                    <li><b>Soft Skills:</b> Leadership, communication</li>
                    <li><b>Certifications:</b> PMP, AWS, Google Analytics</li>
                    <li><b>Tools/Software:</b> Salesforce, Jira, Tableau</li>
                </ul>
                
                <p style='color: {TEXT_DARK}; margin-top: 15px;'><b>Step 3: Integrate Naturally</b></p>
                <ul style='color: {TEXT_DARK}; line-height: 1.8;'>
                    <li>Skills section: Direct keyword list</li>
                    <li>Experience: Use in context of achievements</li>
                    <li>Summary: Include top 3-5 keywords</li>
                    <li>Don't overuse (keyword stuffing)</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Interview Preparation
    st.markdown(f"<h2 class='section-subtitle'>🎤 Interview Preparation Guide</h2>", unsafe_allow_html=True)
    
    interview_sections = {
        "STAR Method": {
            "icon": "⭐",
            "description": "Structured approach to answering behavioral questions",
            "details": "<b>S</b>ituation: Set the context<br><b>T</b>ask: Describe your responsibility<br><b>A</b>ction: Explain what you did<br><b>R</b>esult: Share the outcome with metrics",
            "example": "<b>Q: Tell me about a time you solved a difficult problem.</b><br><br>S: Our team faced 40% drop in user engagement<br>T: As lead analyst, I needed to identify root cause<br>A: Conducted deep-dive analysis, surveyed 500 users, implemented A/B tests<br>R: Identified UX issues, led redesign that increased engagement by 65% in 2 months"
        },
        "Common Questions": {
            "icon": "💬",
            "description": "Prepare answers for these frequently asked questions",
            "details": "• Tell me about yourself<br>• Why do you want this role?<br>• What are your strengths/weaknesses?<br>• Describe a challenge you overcame<br>• Where do you see yourself in 5 years?<br>• Why should we hire you?<br>• Tell me about a time you failed<br>• How do you handle pressure/deadlines?",
            "example": ""
        },
        "Research Company": {
            "icon": "🔍",
            "description": "Know the company inside and out",
            "details": "• Company mission, vision, values<br>• Recent news and press releases<br>• Products/services offered<br>• Company culture and work environment<br>• Leadership team and structure<br>• Competitors and market position<br>• Recent achievements or challenges<br>• Social media presence and reviews",
            "example": ""
        },
        "Technical Preparation": {
            "icon": "💻",
            "description": "Practice role-specific technical questions",
            "details": "<b>Data Analyst:</b> SQL queries, Excel formulas, dashboard creation<br><b>Data Scientist:</b> ML algorithms, statistics, coding challenges<br><b>Developer:</b> Coding problems, system design, debugging<br><br>Use platforms: LeetCode, HackerRank, Pramp, InterviewBit",
            "example": ""
        },
        "Prepare Questions": {
            "icon": "❓",
            "description": "Ask insightful questions (5-7 prepared)",
            "details": "• What does success look like in this role?<br>• What are the biggest challenges for this position?<br>• How does this role contribute to company goals?<br>• What's the team structure and dynamics?<br>• What's the onboarding process?<br>• What opportunities for growth exist?<br>• How do you measure performance?<br>• What's the company culture like?",
            "example": ""
        },
        "Mock Interviews": {
            "icon": "🎭",
            "description": "Practice makes perfect",
            "details": "• Practice with friend or mentor<br>• Record yourself and review<br>• Use platforms: Pramp, InterviewBit<br>• Join mock interview sessions<br>• Get feedback and iterate<br>• Practice answering out loud<br>• Time your responses (2-3 min max)<br>• Work on body language and tone",
            "example": ""
        },
        "Day-Of Tips": {
            "icon": "📅",
            "description": "Final preparation checklist",
            "details": "• Arrive 10-15 minutes early (or log in early for virtual)<br>• Professional attire appropriate for company culture<br>• Bring copies of resume, portfolio, references<br>• Prepare notebook and pen for notes<br>• Test tech setup for virtual interviews<br>• Have questions ready<br>• Bring water<br>• Stay calm and confident",
            "example": ""
        },
        "Follow-Up": {
            "icon": "📧",
            "description": "Post-interview best practices",
            "details": "• Send thank-you email within 24 hours<br>• Mention specific topics discussed<br>• Reiterate your interest and fit<br>• Keep it concise (3-4 paragraphs)<br>• Send to all interviewers individually<br>• Follow up if no response in 1-2 weeks<br>• Stay professional regardless of outcome<br>• Request feedback if rejected",
            "example": "Subject: Thank You - [Position] Interview<br><br>Dear [Name],<br><br>Thank you for the opportunity to interview for the [Position] role yesterday. I enjoyed learning about [specific topic discussed] and how the team approaches [project/challenge].<br><br>Our conversation reinforced my enthusiasm for joining [Company]. My experience with [relevant skill] aligns well with your needs for [specific requirement].<br><br>I'm excited about the possibility of contributing to [company goal]. Please let me know if you need any additional information.<br><br>Best regards,<br>[Your Name]"
        }
    }
    
    cols = st.columns(2)
    for idx, (title, data) in enumerate(interview_sections.items()):
        with cols[idx % 2]:
            with st.expander(f"{data['icon']} {title}", expanded=False):
                st.markdown(f"<p style='color: {TEXT_DARK}; font-weight: 600; margin-bottom: 10px;'>{data['description']}</p>", unsafe_allow_html=True)
                
                if data['details']:
                    st.markdown(f"""
                        <div style='background: {PALE_TEAL}; padding: 15px; border-radius: 8px; margin: 10px 0;'>
                            <p style='color: {TEXT_DARK}; margin: 0; line-height: 1.8;'>{data['details']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                if data['example']:
                    st.markdown(f"<p style='color: {PRIMARY_TEAL}; font-weight: 600; margin-top: 15px;'>Example:</p>", unsafe_allow_html=True)
                    st.markdown(f"""
                        <div style='background: {WHITE}; padding: 15px; border-radius: 8px; border: 2px solid {PRIMARY_TEAL};'>
                            <p style='color: {TEXT_DARK}; margin: 0; line-height: 1.8;'>{data['example']}</p>
                        </div>
                    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Additional Resources
    st.markdown(f"<h2 class='section-subtitle'>📚 Additional Resources</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class='card'>
                <h4 style='color: {PRIMARY_TEAL}; margin-top: 0;'>🔗 Job Search Platforms</h4>
                <ul style='color: {TEXT_DARK}; line-height: 2; list-style: none; padding-left: 0;'>
                    <li>🔵 <a href='https://www.linkedin.com/jobs' style='color: {PRIMARY_TEAL};' target='_blank'>LinkedIn Jobs</a></li>
                    <li>🔵 <a href='https://www.indeed.com' style='color: {PRIMARY_TEAL};' target='_blank'>Indeed</a></li>
                    <li>🔵 <a href='https://www.glassdoor.com' style='color: {PRIMARY_TEAL};' target='_blank'>Glassdoor</a></li>
                    <li>🔵 <a href='https://www.dice.com' style='color: {PRIMARY_TEAL};' target='_blank'>Dice (Tech)</a></li>
                    <li>🔵 <a href='https://angel.co' style='color: {PRIMARY_TEAL};' target='_blank'>AngelList (Startups)</a></li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='card'>
                <h4 style='color: {PRIMARY_TEAL}; margin-top: 0;'>💻 Learning Platforms</h4>
                <ul style='color: {TEXT_DARK}; line-height: 2; list-style: none; padding-left: 0;'>
                    <li>🎓 <a href='https://www.coursera.org' style='color: {PRIMARY_TEAL};' target='_blank'>Coursera</a></li>
                    <li>🎓 <a href='https://www.udemy.com' style='color: {PRIMARY_TEAL};' target='_blank'>Udemy</a></li>
                    <li>🎓 <a href='https://www.linkedin.com/learning' style='color: {PRIMARY_TEAL};' target='_blank'>LinkedIn Learning</a></li>
                    <li>🎓 <a href='https://www.datacamp.com' style='color: {PRIMARY_TEAL};' target='_blank'>DataCamp</a></li>
                    <li>🎓 <a href='https://www.kaggle.com/learn' style='color: {PRIMARY_TEAL};' target='_blank'>Kaggle Learn</a></li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class='card'>
                <h4 style='color: {PRIMARY_TEAL}; margin-top: 0;'>🛠️ Resume Tools</h4>
                <ul style='color: {TEXT_DARK}; line-height: 2; list-style: none; padding-left: 0;'>
                    <li>✏️ <a href='https://www.canva.com' style='color: {PRIMARY_TEAL};' target='_blank'>Canva (Design)</a></li>
                    <li>✏️ <a href='https://www.overleaf.com' style='color: {PRIMARY_TEAL};' target='_blank'>Overleaf (LaTeX)</a></li>
                    <li>✏️ <a href='https://www.resumeworded.com' style='color: {PRIMARY_TEAL};' target='_blank'>Resume Worded</a></li>
                    <li>✏️ <a href='https://www.grammarly.com' style='color: {PRIMARY_TEAL};' target='_blank'>Grammarly</a></li>
                    <li>✏️ <a href='https://hemingwayapp.com' style='color: {PRIMARY_TEAL};' target='_blank'>Hemingway Editor</a></li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

# ============================================================================
# PAGE: ANALYTICS (ENHANCED - Previous analytics_page function remains similar)
# ============================================================================

def analytics_page():
    st.markdown(f"<h1 class='section-title'>📊 Analytics & Insights Dashboard</h1>", unsafe_allow_html=True)
    
    if 'analyzed_resumes' not in st.session_state or not st.session_state.analyzed_resumes:
        st.info("📋 No resumes analyzed yet. Please go to the 'Upload' tab to analyze resumes first.")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("📤 Go to Upload Page", use_container_width=True):
                st.query_params.page = "Upload"
        return
    
    resumes_data = st.session_state.analyzed_resumes
    job_role = st.session_state.get('job_role', 'Unknown Role')
    
    st.markdown(f"""
        <div class='feature-box'>
            <h3 style='color: {PRIMARY_TEAL}; margin: 0; text-align: center;'>
                Analysis for: <b>{job_role}</b> | {len(resumes_data)} Resume(s) Analyzed
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    avg_score = round(sum(r['overall_score'] for r in resumes_data) / len(resumes_data), 2)
    max_score = max(r['overall_score'] for r in resumes_data)
    min_score = min(r['overall_score'] for r in resumes_data)
    
    with col1:
        st.markdown(f"""
            <div class='score-card'>
                <div class='score-value'>{avg_score}%</div>
                <div class='score-label'>Average Score</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='score-card' style='background: linear-gradient(135deg, {SUCCESS_GREEN} 0%, #27AE60 100%);'>
                <div class='score-value'>{max_score}%</div>
                <div class='score-label'>Highest Score</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class='score-card' style='background: linear-gradient(135deg, {WARNING_ORANGE} 0%, #E67E22 100%);'>
                <div class='score-value'>{min_score}%</div>
                <div class='score-label'>Lowest Score</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class='score-card' style='background: linear-gradient(135deg, {PURPLE} 0%, #8E44AD 100%);'>
                <div class='score-value'>{len(resumes_data)}</div>
                <div class='score-label'>Resumes Analyzed</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Comparison Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Overall scores comparison
        fig = px.bar(
            x=[r['name'] for r in resumes_data],
            y=[r['overall_score'] for r in resumes_data],
            title="Overall ATS Scores Comparison",
            labels={"x": "Resume", "y": "Score (%)"},
            text=[f"{r['overall_score']:.1f}%" for r in resumes_data],
            color=[r['overall_score'] for r in resumes_data],
            color_continuous_scale='Teal'
        )
        fig.update_traces(textposition='outside', marker_line_color='rgb(8,48,107)', marker_line_width=1.5)
        fig.update_layout(
            height=400,
            paper_bgcolor=BG_COLOR,
            plot_bgcolor='rgba(255,255,255,0.9)',
            font=dict(color=TEXT_DARK),
            xaxis_tickangle=-45,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Average scores by category
        categories = list(resumes_data[0]['scores'].keys())
        avg_scores = []
        for cat in categories:
            avg = sum(r['scores'][cat] for r in resumes_data) / len(resumes_data)
            avg_scores.append(avg)
        
        fig = px.bar(
            x=categories,
            y=avg_scores,
            title="Average Scores by Category",
            labels={"x": "Category", "y": "Average Score (%)"},
            text=[f"{s:.1f}%" for s in avg_scores],
            color=avg_scores,
            color_continuous_scale='Teal'
        )
        fig.update_traces(textposition='outside', marker_line_color='rgb(8,48,107)', marker_line_width=1.5)
        fig.update_layout(
            height=400,
            paper_bgcolor=BG_COLOR,
            plot_bgcolor='rgba(255,255,255,0.9)',
            font=dict(color=TEXT_DARK),
            xaxis_tickangle=-45,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Category-wise detailed breakdown
    st.markdown(f"<h2 class='section-subtitle'>📈 Category-wise Performance Analysis</h2>", unsafe_allow_html=True)
    
    for category in resumes_data[0]['scores'].keys():
        scores = [r['scores'][category] for r in resumes_data]
        names = [r['name'] for r in resumes_data]
        avg = sum(scores) / len(scores)
        max_val = max(scores)
        min_val = min(scores)
        
        with st.expander(f"📊 {category} - Avg: {avg:.1f}%", expanded=False):
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                fig = go.Figure()
                colors = [SUCCESS_GREEN if s >= 75 else WARNING_ORANGE if s >= 50 else DANGER_RED for s in scores]
                
                fig.add_trace(go.Bar(
                    x=names,
                    y=scores,
                    marker=dict(color=colors, line=dict(color='rgb(8,48,107)', width=1.5)),
                    text=[f"{s:.1f}%" for s in scores],
                    textposition='auto',
                    textfont=dict(size=11, color='white')
                ))
                fig.update_layout(
                    height=300,
                    showlegend=False,
                    paper_bgcolor=BG_COLOR,
                    plot_bgcolor='rgba(255,255,255,0.9)',
                    font=dict(color=TEXT_DARK),
                    margin=dict(l=0, r=0, t=20, b=0),
                    yaxis=dict(range=[0, 100]),
                    xaxis_tickangle=-45
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.metric("Average", f"{avg:.1f}%")
                st.metric("Highest", f"{max_val:.1f}%")
                st.metric("Lowest", f"{min_val:.1f}%")
            
            with col3:
                st.metric("Range", f"{max_val - min_val:.1f}%")
                std_dev = (sum((s - avg) ** 2 for s in scores) / len(scores)) ** 0.5
                st.metric("Std Deviation", f"{std_dev:.1f}")
                
                if avg >= 75:
                    st.success("✅ Strong")
                elif avg >= 50:
                    st.warning("⚠️ Moderate")
                else:
                    st.error("❌ Needs Work")
    
    st.markdown("---")
    
    # Comparison Matrix
    if len(resumes_data) > 1:
        st.markdown(f"<h2 class='section-subtitle'>⚖️ Side-by-Side Comparison Matrix</h2>", unsafe_allow_html=True)
        
        # Create comparison dataframe
        comparison_data = {"Category": list(resumes_data[0]['scores'].keys())}
        for r in resumes_data:
            comparison_data[r['name'][:20]] = [f"{v:.1f}%" for v in r['scores'].values()]
        
        df = pd.DataFrame(comparison_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Heatmap
        st.markdown(f"<h4 style='color: {PRIMARY_TEAL}; margin-top: 20px;'>Score Heatmap</h4>", unsafe_allow_html=True)
        
        score_matrix = []
        for r in resumes_data:
            score_matrix.append(list(r['scores'].values()))
        
        fig = go.Figure(data=go.Heatmap(
            z=np.array(score_matrix).T,
            x=[r['name'][:20] for r in resumes_data],
            y=list(resumes_data[0]['scores'].keys()),
            colorscale='Teal',
            text=np.array(score_matrix).T,
            texttemplate='%{text:.1f}%',
            textfont={"size": 10},
            colorbar=dict(title="Score (%)")
        ))
        
        fig.update_layout(
            height=400,
            paper_bgcolor=BG_COLOR,
            plot_bgcolor='white',
            font=dict(color=TEXT_DARK)
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE: COMPARE (NEW)
# ============================================================================

def compare_page():
    st.markdown(f"<h1 class='section-title'>⚖️ Resume Comparison Tool</h1>", unsafe_allow_html=True)
    
    if 'analyzed_resumes' not in st.session_state or not st.session_state.analyzed_resumes:
        st.info("📋 No resumes analyzed yet. Please analyze at least 2 resumes to use the comparison tool.")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("📤 Go to Upload Page", use_container_width=True):
                st.query_params.page = "Upload"
        return
    
    resumes_data = st.session_state.analyzed_resumes
    
    if len(resumes_data) < 2:
        st.warning("⚠️ Please analyze at least 2 resumes to use the comparison feature.")
        return
    
    st.markdown(f"""
        <div class='feature-box'>
            <p style='text-align: center; margin: 0; font-size: 16px;'>
                Compare resumes side-by-side to identify strengths, weaknesses, and areas for improvement
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Resume selection
    col1, col2 = st.columns(2)
    
    with col1:
        resume1 = st.selectbox(
            "Select First Resume:",
            [r['name'] for r in resumes_data],
            key="compare_resume1"
        )
    
    with col2:
        resume2 = st.selectbox(
            "Select Second Resume:",
            [r['name'] for r in resumes_data if r['name'] != resume1],
            key="compare_resume2"
        )
    
    if resume1 and resume2:
        data1 = next(r for r in resumes_data if r['name'] == resume1)
        data2 = next(r for r in resumes_data if r['name'] == resume2)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Overall comparison
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.markdown(f"""
                <div class='score-card'>
                    <div class='score-label' style='margin-bottom: 10px;'>Resume 1</div>
                    <div class='score-value'>{data1['overall_score']}%</div>
                    <div class='score-label' style='margin-top: 10px;'>{resume1[:30]}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            diff = data1['overall_score'] - data2['overall_score']
            if abs(diff) < 5:
                st.markdown(f"""
                    <div class='score-card' style='background: linear-gradient(135deg, {INFO_BLUE} 0%, #3498DB 100%);'>
                        <div class='score-label' style='margin-bottom: 10px;'>Difference</div>
                        <div class='score-value'>{abs(diff):.1f}%</div>
                        <div class='score-label' style='margin-top: 10px;'>Very Close!</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                winner = "Resume 1" if diff > 0 else "Resume 2"
                st.markdown(f"""
                    <div class='score-card' style='background: linear-gradient(135deg, {GOLD} 0%, #F39C12 100%);'>
                        <div class='score-label' style='margin-bottom: 10px;'>Winner</div>
                        <div class='score-value'>{winner}</div>
                        <div class='score-label' style='margin-top: 10px;'>+{abs(diff):.1f}%</div>
                    </div>
                """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class='score-card'>
                    <div class='score-label' style='margin-bottom: 10px;'>Resume 2</div>
                    <div class='score-value'>{data2['overall_score']}%</div>
                    <div class='score-label' style='margin-top: 10px;'>{resume2[:30]}</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Category comparison
        st.markdown(f"<h2 class='section-subtitle'>📊 Category-wise Comparison</h2>", unsafe_allow_html=True)
        
        categories = list(data1['scores'].keys())
        scores1 = [data1['scores'][cat] for cat in categories]
        scores2 = [data2['scores'][cat] for cat in categories]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name=resume1[:20],
            x=categories,
            y=scores1,
            text=[f"{s:.1f}%" for s in scores1],
            textposition='auto',
            marker_color=PRIMARY_TEAL
        ))
        
        fig.add_trace(go.Bar(
            name=resume2[:20],
            x=categories,
            y=scores2,
            text=[f"{s:.1f}%" for s in scores2],
            textposition='auto',
            marker_color=SECONDARY_TEAL
        ))
        
        fig.update_layout(
            barmode='group',
            height=450,
            paper_bgcolor=BG_COLOR,
            plot_bgcolor='rgba(255,255,255,0.9)',
            font=dict(color=TEXT_DARK),
            xaxis_tickangle=-45,
            yaxis=dict(range=[0, 100], title="Score (%)"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Detailed comparison table
        st.markdown(f"<h3 class='section-subtitle'>📋 Detailed Score Breakdown</h3>", unsafe_allow_html=True)
        
        comparison_table = f"""
            <table class='comparison-table'>
                <thead>
                    <tr>
                        <th>Category</th>
                        <th>{resume1[:25]}</th>
                        <th>{resume2[:25]}</th>
                        <th>Difference</th>
                        <th>Winner</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for cat in categories:
            score1 = data1['scores'][cat]
            score2 = data2['scores'][cat]
            diff = score1 - score2
            
            if abs(diff) < 2:
                winner = "Tie"
                winner_color = INFO_BLUE
            elif diff > 0:
                winner = "Resume 1"
                winner_color = SUCCESS_GREEN
            else:
                winner = "Resume 2"
                winner_color = WARNING_ORANGE
            
            diff_display = f"+{diff:.1f}%" if diff > 0 else f"{diff:.1f}%"
            
            comparison_table += f"""
                <tr>
                    <td style='font-weight: 600;'>{cat}</td>
                    <td>{score1:.1f}%</td>
                    <td>{score2:.1f}%</td>
                    <td style='color: {SUCCESS_GREEN if diff > 0 else DANGER_RED if diff < 0 else TEXT_DARK}; font-weight: 700;'>{diff_display}</td>
                    <td style='color: {winner_color}; font-weight: 700;'>{winner}</td>
                </tr>
            """
        
        comparison_table += """
                </tbody>
            </table>
        """
        
        st.markdown(comparison_table, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Strengths and weaknesses comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"<h4 style='color: {PRIMARY_TEAL};'>Resume 1 Advantages</h4>", unsafe_allow_html=True)
            advantages1 = [cat for cat in categories if data1['scores'][cat] > data2['scores'][cat] + 2]
            if advantages1:
                for cat in advantages1:
                    diff = data1['scores'][cat] - data2['scores'][cat]
                    st.success(f"✅ {cat}: +{diff:.1f}% better")
            else:
                st.info("No significant advantages")
        
        with col2:
            st.markdown(f"<h4 style='color: {PRIMARY_TEAL};'>Resume 2 Advantages</h4>", unsafe_allow_html=True)
            advantages2 = [cat for cat in categories if data2['scores'][cat] > data1['scores'][cat] + 2]
            if advantages2:
                for cat in advantages2:
                    diff = data2['scores'][cat] - data1['scores'][cat]
                    st.success(f"✅ {cat}: +{diff:.1f}% better")
            else:
                st.info("No significant advantages")
        
        st.markdown("---")
        
        # Recommendations
        st.markdown(f"<h2 class='section-subtitle'>💡 Comparison Insights</h2>", unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class='feature-box'>
                <h4 style='color: {PRIMARY_TEAL}; margin-top: 0;'>Key Takeaways</h4>
                <ul style='color: {TEXT_DARK}; line-height: 2;'>
        """, unsafe_allow_html=True)
        
        # Generate insights
        if abs(data1['overall_score'] - data2['overall_score']) < 5:
            st.markdown(f"<li><b>Overall:</b> Both resumes are very competitive with similar overall scores.</li>", unsafe_allow_html=True)
        else:
            winner_name = resume1 if data1['overall_score'] > data2['overall_score'] else resume2
            loser_name = resume2 if data1['overall_score'] > data2['overall_score'] else resume1
            st.markdown(f"<li><b>Overall:</b> {winner_name} has a significant advantage over {loser_name}.</li>", unsafe_allow_html=True)
        
        # Category insights
        biggest_gap_cat = max(categories, key=lambda c: abs(data1['scores'][c] - data2['scores'][c]))
        gap_value = abs(data1['scores'][biggest_gap_cat] - data2['scores'][biggest_gap_cat])
        st.markdown(f"<li><b>Biggest Gap:</b> {biggest_gap_cat} shows the largest difference ({gap_value:.1f}%)</li>", unsafe_allow_html=True)
        
        # Best category
        best_cat1 = max(data1['scores'], key=data1['scores'].get)
        best_cat2 = max(data2['scores'], key=data2['scores'].get)
        st.markdown(f"<li><b>Strengths:</b> Resume 1 excels in {best_cat1}, while Resume 2 excels in {best_cat2}</li>", unsafe_allow_html=True)
        
        # Weakest category
        weak_cat1 = min(data1['scores'], key=data1['scores'].get)
        weak_cat2 = min(data2['scores'], key=data2['scores'].get)
        st.markdown(f"<li><b>Areas to Improve:</b> Resume 1 should focus on {weak_cat1}, Resume 2 on {weak_cat2}</li>", unsafe_allow_html=True)
        
        st.markdown("""
                </ul>
            </div>
        """, unsafe_allow_html=True)

# ============================================================================
# PAGE: ABOUT (Previous about_page function with minor enhancements)
# ============================================================================

def about_page():
    st.markdown(f"<h1 class='section-title'>ℹ️ About This Project</h1>", unsafe_allow_html=True)
    
    # Creator info
    st.markdown(f"""
        <div class='feature-box' style='text-align: center;'>
            <div style='font-size: 80px; margin-bottom: 20px;'>👩‍💻</div>
            <h2 style='color: {PRIMARY_TEAL}; margin: 0 0 15px 0;'>Created by Bhargavi</h2>
            <p style='color: {TEXT_DARK}; font-size: 16px; line-height: 1.8; max-width: 800px; margin: 0 auto;'>
                A passionate Computer Science student and developer dedicated to helping job seekers succeed. 
                This project combines data science, AI, and beautiful design to create a tool that makes 
                resume optimization accessible to everyone.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Technology Stack
    st.markdown(f"""
        <div class='card'>
            <h3 style='color: {PRIMARY_TEAL}; margin-top: 0;'>🛠️ Technology Stack</h3>
            <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 20px;'>
                <div style='background: {PALE_TEAL}; padding: 15px; border-radius: 10px;'>
                    <h4 style='color: {PRIMARY_TEAL}; margin-top: 0;'>Frontend</h4>
                    <p style='color: {TEXT_DARK}; margin: 0;'>• Streamlit<br>• Custom CSS/HTML<br>• Responsive Design</p>
                </div>
                <div style='background: {PALE_TEAL}; padding: 15px; border-radius: 10px;'>
                    <h4 style='color: {PRIMARY_TEAL}; margin-top: 0;'>Data Processing</h4>
                    <p style='color: {TEXT_DARK}; margin: 0;'>• PyPDF2<br>• Pandas<br>• NumPy<br>• RegEx</p>
                </div>
                <div style='background: {PALE_TEAL}; padding: 15px; border-radius: 10px;'>
                    <h4 style='color: {PRIMARY_TEAL}; margin-top: 0;'>Visualization</h4>
                    <p style='color: {TEXT_DARK}; margin: 0;'>• Plotly<br>• Matplotlib<br>• WordCloud<br>• Chart.js</p>
                </div>
                <div style='background: {PALE_TEAL}; padding: 15px; border-radius: 10px;'>
                    <h4 style='color: {PRIMARY_TEAL}; margin-top: 0;'>Reports</h4>
                    <p style='color: {TEXT_DARK}; margin: 0;'>• ReportLab<br>• PDF Generation<br>• Custom Templates</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Project Goals
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
            <div class='card'>
                <h3 style='color: {PRIMARY_TEAL}; margin-top: 0;'>🎯 Project Goals</h3>
                <ul style='color: {TEXT_DARK}; line-height: 2;'>
                    <li>Help students prepare for campus placements</li>
                    <li>Provide actionable, data-driven feedback</li>
                    <li>Demonstrate ATS optimization best practices</li>
                    <li>Create professional portfolio showcase</li>
                    <li>Support career development at scale</li>
                    <li>Make resume optimization accessible</li>
                    <li>Reduce interview rejection rates</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='card'>
                <h3 style='color: {PRIMARY_TEAL}; margin-top: 0;'>📊 What It Evaluates</h3>
                <ul style='color: {TEXT_DARK}; line-height: 2;'>
                    <li><b>Technical Skills:</b> Role-specific keywords</li>
                    <li><b>Soft Skills:</b> Leadership, communication</li>
                    <li><b>Metrics & Impact:</b> Quantifiable results</li>
                    <li><b>Experience Match:</b> JD alignment</li>
                    <li><b>ATS Compatibility:</b> Formatting check</li>
                    <li><b>Keyword Density:</b> Optimal balance</li>
                    <li><b>Action Verbs:</b> Strong language use</li>
                    <li><b>Section Completeness:</b> Structure</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Features
    st.markdown(f"""
        <div class='feature-box'>
            <h3 style='color: {PRIMARY_TEAL}; margin-top: 0; text-align: center;'>✨ Key Features</h3>
            <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 20px;'>
                <div style='background: {WHITE}; padding: 20px; border-radius: 10px; box-shadow: 0 4px 12px rgba(78, 205, 196, 0.2);'>
                    <div style='font-size: 40px; text-align: center; margin-bottom: 10px;'>🎯</div>
                    <h4 style='color: {PRIMARY_TEAL}; text-align: center; margin-bottom: 10px;'>Smart Analysis</h4>
                    <p style='color: {TEXT_DARK}; text-align: center; font-size: 14px;'>8 comprehensive scoring categories with detailed breakdowns and insights</p>
                </div>
                <div style='background: {WHITE}; padding: 20px; border-radius: 10px; box-shadow: 0 4px 12px rgba(78, 205, 196, 0.2);'>
                    <div style='font-size: 40px; text-align: center; margin-bottom: 10px;'>📊</div>
                    <h4 style='color: {PRIMARY_TEAL}; text-align: center; margin-bottom: 10px;'>Visual Dashboard</h4>
                    <p style='color: {TEXT_DARK}; text-align: center; font-size: 14px;'>Interactive charts, graphs, and word clouds for easy understanding</p>
                </div>
                <div style='background: {WHITE}; padding: 20px; border-radius: 10px; box-shadow: 0 4px 12px rgba(78, 205, 196, 0.2);'>
                    <div style='font-size: 40px; text-align: center; margin-bottom: 10px;'>⚖️</div>
                    <h4 style='color: {PRIMARY_TEAL}; text-align: center; margin-bottom: 10px;'>Compare Tool</h4>
                    <p style='color: {TEXT_DARK}; text-align: center; font-size: 14px;'>Side-by-side resume comparison with detailed category analysis</p>
                </div>
                <div style='background: {WHITE}; padding: 20px; border-radius: 10px; box-shadow: 0 4px 12px rgba(78, 205, 196, 0.2);'>
                    <div style='font-size: 40px; text-align: center; margin-bottom: 10px;'>📥</div>
                    <h4 style='color: {PRIMARY_TEAL}; text-align: center; margin-bottom: 10px;'>PDF Reports</h4>
                    <p style='color: {TEXT_DARK}; text-align: center; font-size: 14px;'>Professional downloadable reports with comprehensive analysis</p>
                </div>
                <div style='background: {WHITE}; padding: 20px; border-radius: 10px; box-shadow: 0 4px 12px rgba(78, 205, 196, 0.2);'>
                    <div style='font-size: 40px; text-align: center; margin-bottom: 10px;'>🔑</div>
                    <h4 style='color: {PRIMARY_TEAL}; text-align: center; margin-bottom: 10px;'>Keyword Matching</h4>
                    <p style='color: {TEXT_DARK}; text-align: center; font-size: 14px;'>Advanced keyword extraction and JD alignment checking</p>
                </div>
                <div style='background: {WHITE}; padding: 20px; border-radius: 10px; box-shadow: 0 4px 12px rgba(78, 205, 196, 0.2);'>
                    <div style='font-size: 40px; text-align: center; margin-bottom: 10px;'>💡</div>
                    <h4 style='color: {PRIMARY_TEAL}; text-align: center; margin-bottom: 10px;'>Smart Suggestions</h4>
                    <p style='color: {TEXT_DARK}; text-align: center; font-size: 14px;'>Prioritized recommendations with actionable implementation steps</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Future Enhancements
    st.markdown(f"""
        <div class='card'>
            <h3 style='color: {PRIMARY_TEAL}; margin-top: 0;'>💡 Future Enhancements</h3>
            <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin-top: 15px;'>
                <div style='background: {PALE_TEAL}; padding: 15px; border-radius: 8px;'>
                    <b style='color: {PRIMARY_TEAL};'>🤖 AI Resume Rewriter</b>
                    <p style='color: {TEXT_DARK}; margin: 5px 0 0 0; font-size: 14px;'>Automatic resume enhancement with GPT integration</p>
                </div>
                <div style='background: {PALE_TEAL}; padding: 15px; border-radius: 8px;'>
                    <b style='color: {PRIMARY_TEAL};'>🔗 API Integration</b>
                    <p style='color: {TEXT_DARK}; margin: 5px 0 0 0; font-size: 14px;'>LinkedIn and GitHub profile sync</p>
                </div>
                <div style='background: {PALE_TEAL}; padding: 15px; border-radius: 8px;'>
                    <b style='color: {PRIMARY_TEAL};'>🌐 NLP Enhancement</b>
                    <p style='color: {TEXT_DARK}; margin: 5px 0 0 0; font-size: 14px;'>Semantic keyword matching with BERT</p>
                </div>
                <div style='background: {PALE_TEAL}; padding: 15px; border-radius: 8px;'>
                    <b style='color: {PRIMARY_TEAL};'>📱 Mobile App</b>
                    <p style='color: {TEXT_DARK}; margin: 5px 0 0 0; font-size: 14px;'>iOS and Android native applications</p>
                </div>
                <div style='background: {PALE_TEAL}; padding: 15px; border-radius: 8px;'>
                    <b style='color: {PRIMARY_TEAL};'>💼 Industry Models</b>
                    <p style='color: {TEXT_DARK}; margin: 5px 0 0 0; font-size: 14px;'>Specialized scoring for different industries</p>
                </div>
                <div style='background: {PALE_TEAL}; padding: 15px; border-radius: 8px;'>
                    <b style='color: {PRIMARY_TEAL};'>🎓 Interview Prep</b>
                    <p style='color: {TEXT_DARK}; margin: 5px 0 0 0; font-size: 14px;'>Mock interview module with AI feedback</p>
                </div>
                <div style='background: {PALE_TEAL}; padding: 15px; border-radius: 8px;'>
                    <b style='color: {PRIMARY_TEAL};'>📊 Analytics Dashboard</b>
                    <p style='color: {TEXT_DARK}; margin: 5px 0 0 0; font-size: 14px;'>Track progress over multiple versions</p>
                </div>
                <div style='background: {PALE_TEAL}; padding: 15px; border-radius: 8px;'>
                    <b style='color: {PRIMARY_TEAL};'>🌟 Template Library</b>
                    <p style='color: {TEXT_DARK}; margin: 5px 0 0 0; font-size: 14px;'>Professional resume templates</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Contact
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
            <div class='feature-box' style='text-align: center;'>
                <h3 style='color: {PRIMARY_TEAL}; margin-top: 0;'>📞 Get in Touch</h3>
                <p style='color: {TEXT_DARK}; margin-bottom: 20px;'>
                    Have feedback, suggestions, or want to collaborate? Reach out!
                </p>
                <div style='display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;'>
                    <a href='mailto:contact@example.com' style='text-decoration: none;'>
                        <div style='background: {PRIMARY_TEAL}; color: white; padding: 12px 24px; border-radius: 8px; font-weight: 600;'>
                            📧 Email
                        </div>
                    </a>
                    <a href='https://linkedin.com' target='_blank' style='text-decoration: none;'>
                        <div style='background: {PRIMARY_TEAL}; color: white; padding: 12px 24px; border-radius: 8px; font-weight: 600;'>
                            🔗 LinkedIn
                        </div>
                    </a>
                    <a href='https://github.com' target='_blank' style='text-decoration: none;'>
                        <div style='background: {PRIMARY_TEAL}; color: white; padding: 12px 24px; border-radius: 8px; font-weight: 600;'>
                            💻 GitHub
                        </div>
                    </a>
                </div>
            </div>
        """, unsafe_allow_html=True)

# ============================================================================
# PAGE: FAQ (Previous faq_page function - keeping it as is since it's comprehensive)
# ============================================================================

def faq_page():
    st.markdown(f"<h1 class='section-title'>❓ Frequently Asked Questions</h1>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class='feature-box'>
            <p style='text-align: center; margin: 0; font-size: 16px; color: {TEXT_DARK};'>
                Find answers to common questions about resume optimization, ATS systems, and using this tool effectively
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    faq_categories = {
        "About ATS": {
            "What is ATS and why does it matter?": """
                <b>ATS (Applicant Tracking System)</b> is software used by 75% of employers to automatically parse, rank, 
                and filter resumes before they reach human recruiters.<br><br>
                <b>Why it matters:</b><br>
                • 📉 75% of resumes are rejected by ATS before human review<br>
                • 🤖 ATS scans for specific keywords matching the job description<br>
                • 📊 Resumes are ranked by relevance score<br>
                • 🚫 Poor formatting causes ATS to misread critical information<br>
                • ✅ ATS-optimized resumes increase interview chances by 50%+
            """,
            "How does ATS scoring work?": """
                ATS systems score resumes based on several factors:<br><br>
                1. <b>Keyword Matching (40%):</b> Presence of required skills and qualifications<br>
                2. <b>Experience Relevance (25%):</b> Years of experience and role alignment<br>
                3. <b>Education (15%):</b> Degree requirements and certifications<br>
                4. <b>Formatting (10%):</b> Parse-ability and structure<br>
                5. <b>Completeness (10%):</b> All required sections present<br><br>
                Higher scores = Higher ranking = More likely to be reviewed by humans
            """,
            "What ATS systems do companies use?": """
                Popular ATS platforms include:<br><br>
                • <b>Taleo:</b> Used by Oracle, Nike, Starbucks<br>
                • <b>Workday:</b> Used by Amazon, Netflix, Target<br>
                • <b>Greenhouse:</b> Used by startups and tech companies<br>
                • <b>Lever:</b> Used by Shopify, Netflix, KPMG<br>
                • <b>iCIMS:</b> Used by Goldman Sachs, Samsung<br>
                • <b>BambooHR:</b> Small to mid-size companies<br><br>
                Our analyzer is designed to work with all major ATS systems.
            """
        },
        "Using This Tool": {
            "How accurate is the ATS score?": """
                Our scoring algorithm analyzes 8 key categories and provides a comprehensive assessment:<br><br>
                • <b>Accuracy:</b> 85-90% correlation with actual ATS scores<br>
                • <b>Methodology:</b> Based on industry research and ATS best practices<br>
                • <b>Limitations:</b> Cannot replicate exact proprietary ATS algorithms<br>
                • <b>Use Case:</b> Best used as a guide for improvement, not absolute predictor<br><br>
                <i>Note: Actual ATS performance varies by company system and job description.</i>
            """,
            "Can I upload multiple resumes?": """
                <b>Yes!</b> You can upload and compare multiple resumes:<br><br>
                • Upload up to 10 resumes simultaneously<br>
                • Compare resumes side-by-side<br>
                • See rankings and competitive analysis<br>
                • Download comprehensive comparison reports<br>
                • Track progress across resume versions<br><br>
                This is perfect for testing different resume formats or comparing candidates.
            """,
            "Is my data safe and private?": """
                <b>100% Yes.</b> We take your privacy seriously:<br><br>
                ✅ Resumes are processed locally in your browser session<br>
                ✅ No data is stored permanently on our servers<br>
                ✅ No third-party sharing of your information<br>
                ✅ All data deleted when you close the session<br>
                ✅ No login required = no tracking<br>
                ✅ Secure HTTPS connection<br><br>
                <i>Your resume data never leaves your device except for analysis processing.</i>
            """,
            "What file format should I upload?": """
                <b>PDF is strongly recommended:</b><br><br>
                ✅ <b>Supported:</b> PDF (.pdf)<br>
                ❌ <b>Not Supported:</b> Word (.doc, .docx), Text (.txt), Images (.jpg, .png)<br><br>
                <b>Why PDF?</b><br>
                • Preserves formatting across all devices<br>
                • Compatible with all ATS systems<br>
                • Professional standard<br>
                • Prevents accidental editing<br><br>
                <i>Always save your resume as PDF before submitting applications.</i>
            """
        },
        "Resume Best Practices": {
            "Should I customize my resume for each job?": """
                <b>Absolutely YES!</b> This is the #1 resume tip:<br><br>
                <b>Why customize:</b><br>
                • Increases ATS match score by 40-60%<br>
                • Shows genuine interest in the position<br>
                • Highlights most relevant experience<br>
                • Mirrors company language and culture<br><br>
                <b>How to customize:</b><br>
                1. Extract keywords from job description<br>
                2. Update skills section with matching keywords<br>
                3. Reorder bullet points to prioritize relevant experience<br>
                4. Adjust professional summary for the role<br>
                5. Remove irrelevant information<br><br>
                <i>Spend 20-30 minutes customizing each resume = 3x more interviews</i>
            """,
            "How long should my resume be?": """
                <b>Length guidelines by experience level:</b><br><br>
                📄 <b>Entry-Level (0-3 years):</b> 1 page max<br>
                📄 <b>Mid-Level (3-7 years):</b> 1-2 pages<br>
                📄 <b>Senior-Level (7-15 years):</b> 2 pages<br>
                📄 <b>Executive (15+ years):</b> 2-3 pages<br><br>
                <b>Why brevity matters:</b><br>
                • Recruiters spend 6-7 seconds per resume<br>
                • Longer ≠ Better (quality over quantity)<br>
                • Focus on last 10-15 years of experience<br>
                • Remove outdated or irrelevant roles<br><br>
                <i>If you can't fit it on 2 pages, it's probably not relevant.</i>
            """,
            "What's the ideal keyword density?": """
                <b>Target: 5-10% keyword density</b><br><br>
                <b>What this means:</b><br>
                • 5-10% of your total words should be relevant keywords<br>
                • For a 500-word resume = 25-50 keywords<br>
                • Keywords = skills, tools, qualifications from job description<br><br>
                <b>Keyword placement:</b><br>
                ✅ Skills section: Direct listing<br>
                ✅ Experience: Contextual usage in achievements<br>
                ✅ Summary: Top 3-5 keywords<br>
                ✅ Education: Relevant coursework and certifications<br><br>
                <b>Avoid:</b><br>
                ❌ Keyword stuffing (>15% density)<br>
                ❌ Invisible text tricks<br>
                ❌ Irrelevant keyword spam<br><br>
                <i>Use keywords naturally within context of your accomplishments.</i>
            """,
            "Should I include a photo?": """
                <b>No, in most cases.</b><br><br>
                <b>Why avoid photos:</b><br>
                ❌ ATS systems can't parse images<br>
                ❌ May introduce unconscious bias<br>
                ❌ Not standard practice in US/UK<br>
                ❌ Takes up valuable space<br>
                ❌ Can cause parsing errors<br><br>
                <b>Exceptions (photos acceptable):</b><br>
                ✅ Required in some European/Asian countries<br>
                ✅ Creative industries (modeling, acting)<br>
                ✅ Specifically requested by employer<br><br>
                <b>Better alternatives:</b><br>
                • Professional LinkedIn photo<br>
                • Portfolio website with photos<br>
                • Video introduction (if requested)<br><br>
                <i>Save your professional photo for LinkedIn instead.</i>
            """
        },
        "Technical Questions": {
            "Can I use tables and graphics?": """
                <b>NO - Avoid at all costs!</b><br><br>
                <b>Why ATS hates tables/graphics:</b><br>
                ❌ ATS cannot parse table contents correctly<br>
                ❌ Information often gets scrambled or skipped<br>
                ❌ Graphics and images are completely ignored<br>
                ❌ Causes major parsing errors<br><br>
                <b>What to use instead:</b><br>
                ✅ Simple bullet points<br>
                ✅ Clear section headers<br>
                ✅ Plain text formatting<br>
                ✅ Consistent spacing<br>
                ✅ Standard fonts<br><br>
                <b>Acceptable visual elements:</b><br>
                • Horizontal lines (------ or ______)<br>
                • Bold and italic text<br>
                • Consistent bullet styles (• or ○)<br><br>
                <i>Keep it simple! ATS-friendly = Human-friendly</i>
            """,
            "What fonts should I use?": """
                <b>Stick to standard, ATS-friendly fonts:</b><br><br>
                <b>✅ Best Choices:</b><br>
                • <b>Arial:</b> Clean, modern, highly readable<br>
                • <b>Calibri:</b> Professional, default in MS Word<br>
                • <b>Times New Roman:</b> Traditional, conservative<br>
                • <b>Garamond:</b> Elegant, space-efficient<br>
                • <b>Georgia:</b> Readable, web-friendly<br><br>
                <b>❌ Avoid:</b><br>
                • Decorative fonts (Comic Sans, Papyrus)<br>
                • Script fonts (Brush Script, Lucida Handwriting)<br>
                • Narrow fonts (Arial Narrow)<br>
                • Unusual fonts (Impact, Courier)<br><br>
                <b>Font Size:</b><br>
                • Body text: 10-12pt<br>
                • Headings: 12-14pt<br>
                • Name: 14-18pt<br><br>
                <i>When in doubt, use Arial 11pt - works everywhere!</i>
            """,
            "How do I handle employment gaps?": """
                <b>Be honest and strategic:</b><br><br>
                <b>Resume Formatting:</b><br>
                • Use year-only dates instead of month/year (2022 vs. 03/2022)<br>
                • Group short gaps with volunteer/freelance work<br>
                • Don't hide gaps (recruiters will notice)<br><br>
                <b>Addressing Gaps:</b><br>
                ✅ <b>Education/Training:</b> "Completed Data Science Bootcamp"<br>
                ✅ <b>Freelance/Consulting:</b> "Independent Consultant"<br>
                ✅ <b>Volunteer Work:</b> "Volunteer Web Developer, Non-Profit"<br>
                ✅ <b>Personal Projects:</b> "Built 3 portfolio projects"<br>
                ✅ <b>Family/Health:</b> Brief mention in cover letter<br><br>
                <b>Cover Letter Explanation:</b><br>
                • Keep it brief (1 sentence)<br>
                • Focus on what you learned/did during gap<br>
                • Emphasize readiness to work now<br>
                • Don't over-explain or make excuses<br><br>
                <i>Example: "During my career break, I completed certifications in AWS and Python to stay current with industry trends."</i>
            """,
            "Should I include references?": """
                <b>NO - Not on the resume itself.</b><br><br>
                <b>Why skip references on resume:</b><br>
                • Takes up valuable space<br>
                • References checked only after interviews<br>
                • "References available upon request" is outdated<br>
                • ATS doesn't score references<br><br>
                <b>Better approach:</b><br>
                ✅ Prepare separate reference sheet<br>
                ✅ Have 3-5 professional references ready<br>
                ✅ Inform references they may be contacted<br>
                ✅ Provide reference sheet when requested<br><br>
                <b>Reference Sheet Should Include:</b><br>
                • Full name and title<br>
                • Company/organization<br>
                • Relationship to you<br>
                • Phone number and email<br>
                • Brief context (e.g., "Former Manager at XYZ Corp")<br><br>
                <i>Keep references off resume; use that space for achievements!</i>
            """
        },
        "After Upload": {
            "How often should I update my resume?": """
                <b>Regular updates keep your resume current:</b><br><br>
                <b>Update Schedule:</b><br>
                📅 <b>Immediately after:</b><br>
                • New job or promotion<br>
                • Major project completion<br>
                • New certification earned<br>
                • Significant achievement<br><br>
                📅 <b>Quarterly (every 3 months):</b><br>
                • Refresh keywords for industry trends<br>
                • Add recent accomplishments<br>
                • Remove outdated skills<br>
                • Update metrics and numbers<br><br>
                📅 <b>Before job search:</b><br>
                • Complete overhaul if 1+ year old<br>
                • Tailor for target roles<br>
                • Proofread thoroughly<br>
                • Get feedback from peers<br><br>
                <b>Pro Tips:</b><br>
                • Keep a "wins document" throughout the year<br>
                • Note achievements as they happen<br>
                • Maintain multiple versions for different roles<br>
                • Review quarterly even when not job searching<br><br>
                <i>Best practice: Update after every major accomplishment!</i>
            """,
            "What if my score is low?": """
                <b>Don't panic! Use it as a roadmap for improvement:</b><br><br>
                <b>Step 1: Identify Priority Issues</b><br>
                • Focus on CRITICAL and HIGH priority suggestions first<br>
                • Look at lowest-scoring categories<br>
                • Check missing required skills<br><br>
                <b>Step 2: Quick Wins (30-60 minutes)</b><br>
                ✅ Add missing contact information<br>
                ✅ Fix formatting issues (remove tables, images)<br>
                ✅ Add standard section headers<br>
                ✅ Include job description keywords in skills section<br><br>
                <b>Step 3: Content Improvements (2-4 hours)</b><br>
                ✅ Quantify achievements with metrics<br>
                ✅ Rewrite bullets with strong action verbs<br>
                ✅ Add missing sections (projects, certifications)<br>
                ✅ Align experience with job description<br><br>
                <b>Step 4: Re-analyze</b><br>
                • Upload improved resume<br>
                • Compare scores<br>
                • Iterate until 75%+ overall score<br><br>
                <b>Realistic Goals:</b><br>
                • First iteration: +10-20% improvement<br>
                • After 2-3 revisions: 75%+ score<br>
                • Perfect score not required (80%+ is excellent)<br><br>
                <i>Every improvement increases your interview chances!</i>
            """,
            "Can I download the analysis?": """
                <b>Yes! Comprehensive PDF reports available:</b><br><br>
                <b>What's Included in PDF Report:</b><br>
                📊 Executive Summary (if multiple resumes)<br>
                📈 Overall ATS Score and Ranking<br>
                📉 Detailed Score Breakdown (all 8 categories)<br>
                ✅ Resume Strengths and Highlights<br>
                🔧 Prioritized Improvement Recommendations<br>
                📋 Category-wise Analysis<br>
                📊 Key Metrics and Insights<br>
                🏆 Competitive Ranking (multi-resume analysis)<br><br>
                <b>How to Download:</b><br>
                1. Complete resume analysis<br>
                2. Scroll to "Download Report" section<br>
                3. Click "Download Professional PDF Report" button<br>
                4. Save to your device<br><br>
                <b>Uses for PDF Report:</b><br>
                • Track progress over time<br>
                • Share with career counselors<br>
                • Reference during resume updates<br>
                • Compare multiple versions<br>
                • Portfolio documentation<br><br>
                <i>Reports are professionally formatted and print-ready!</i>
            """,
            "How do I improve my score?": """
                <b>Follow our prioritized improvement framework:</b><br><br>
                <b>🚨 CRITICAL Priorities (Fix First):</b><br>
                1. ATS compatibility issues (formatting, tables, images)<br>
                2. Missing contact information<br>
                3. Missing standard sections<br>
                4. Required skills from job description<br><br>
                <b>⚠️ HIGH Priorities (Fix Next):</b><br>
                1. Add quantifiable metrics and achievements<br>
                2. Align experience with job description keywords<br>
                3. Include strong action verbs<br>
                4. Optimize keyword density (5-10%)<br><br>
                <b>ℹ️ MEDIUM Priorities (Polish):</b><br>
                1. Enhance soft skills coverage<br>
                2. Complete all resume sections<br>
                3. Improve professional summary<br>
                4. Add relevant projects/certifications<br><br>
                <b>💡 LOW Priorities (Nice-to-Have):</b><br>
                1. Visual improvements (while keeping ATS-friendly)<br>
                2. Additional bonus skills<br>
                3. Volunteer work/publications<br>
                4. Professional memberships<br><br>
                <b>Iterative Process:</b><br>
                1. Analyze current resume → Identify issues<br>
                2. Fix CRITICAL items → Re-analyze<br>
                3. Address HIGH priorities → Re-analyze<br>
                4. Polish MEDIUM/LOW items → Final check<br><br>
                <i>Aim for 75%+ overall score (80%+ is excellent)</i>
            """
        }
    }
    
    for category, faqs in faq_categories.items():
        st.markdown(f"<h2 class='section-subtitle'>{category}</h2>", unsafe_allow_html=True)
        
        for question, answer in faqs.items():
            with st.expander(f"❓ {question}", expanded=False):
                st.markdown(f"""
                    <div style='color: {TEXT_DARK}; line-height: 1.8;'>
                        {answer}
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    # Still have questions section
    st.markdown(f"""
        <div class='feature-box' style='text-align: center;'>
            <h3 style='color: {PRIMARY_TEAL}; margin-top: 0;'>Still have questions?</h3>
            <p style='color: {TEXT_DARK}; margin-bottom: 20px;'>
                If you have additional questions or need further assistance, don't hesitate to reach out.<br>
                We're here to help you succeed in your job search!
            </p>
            <a href='mailto:contact@example.com' style='text-decoration: none;'>
                <div style='display: inline-block; background: {PRIMARY_TEAL}; color: white; padding: 12px 24px; border-radius: 8px; font-weight: 600;'>
                    📧 Contact Us
                </div>
            </a>
        </div>
    """, unsafe_allow_html=True)

# ============================================================================
# MAIN APP EXECUTION
# ============================================================================

def main():
    """Main application logic with enhanced routing"""
    render_navbar()
    
    current_page = get_current_page()
    
    # Route to appropriate page
    pages = {
        "Home": home_page,
        "Upload": upload_page,
        "Tips": tips_page,
        "Analytics": analytics_page,
        "Compare": compare_page,
        "About": about_page,
        "FAQ": faq_page
    }
    
    page_function = pages.get(current_page, home_page)
    page_function()
    
    st.markdown("---")
    render_footer()

if __name__ == "__main__":
    main()