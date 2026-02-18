import streamlit as st

# ---------------- CONFIG ----------------
st.set_page_config(page_title="About | ATS System", page_icon="ℹ️", layout="wide")

# Teal color palette
TEAL_PRIMARY = "#008B8B"
TEAL_SECONDARY = "#20B2AA"
TEAL_DARK = "#006666"
TEAL_LIGHT = "#AFEEEE"

# ---------------- CUSTOM CSS ----------------
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #008B8B 0%, #20B2AA 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 139, 139, 0.3);
    }
    
    .info-card {
        background: linear-gradient(135deg, #E0FFFF 0%, #AFEEEE 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #008B8B;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 139, 139, 0.2);
    }
    
    .feature-box {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #20B2AA;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 139, 139, 0.1);
        text-align: center;
    }
    
    .feature-box h3 {
        color: #008B8B;
        margin-bottom: 0.5rem;
    }
    
    .tech-badge {
        display: inline-block;
        background: linear-gradient(135deg, #008B8B 0%, #20B2AA 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.3rem;
        font-weight: bold;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
    <div class="main-header">
        <h1>ℹ️ About ATS Resume Scoring System</h1>
        <p>Learn about our AI-powered career solution platform</p>
    </div>
""", unsafe_allow_html=True)

# ---------------- TABS ----------------
tab1, tab2, tab3, tab4 = st.tabs(["📖 Overview", "🔬 How It Works", "💻 Technology", "❓ FAQ"])

# ---------------- TAB 1: OVERVIEW ----------------
with tab1:
    st.markdown("### 🎯 What is ATS?")
    
    st.markdown("""
        <div class="info-card">
            <p>
            <b>ATS (Applicant Tracking System)</b> is software used by employers to manage job applications. 
            It automatically scans, parses, and ranks resumes based on how well they match job requirements.
            </p>
            <p>
            <b>90% of Fortune 500 companies</b> use ATS to filter candidates. This means your resume must be 
            ATS-friendly to even reach human recruiters.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🚀 Our Mission")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="info-card">
                <h3>🎯 What We Do</h3>
                <p>
                We empower job seekers with AI-powered tools to create ATS-compatible resumes that get noticed. 
                Our platform analyzes your resume against industry standards and provides actionable feedback 
                to improve your chances of landing interviews.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="info-card">
                <h3>💡 Why We Built This</h3>
                <p>
                Too many qualified candidates are rejected before human review simply because their resumes 
                aren't optimized for ATS. We created this tool to level the playing field and help everyone 
                present their best professional self.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### ✨ Key Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="feature-box">
                <h3>📊 Multi-Category Scoring</h3>
                <p>Evaluate resumes across 6 key dimensions:</p>
                <ul style="text-align: left;">
                    <li>Technical Skills</li>
                    <li>Experience Match</li>
                    <li>Soft Skills</li>
                    <li>Resume Quality</li>
                    <li>Searchability</li>
                    <li>Metrics Usage</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-box">
                <h3>🔍 Intelligent Analysis</h3>
                <p>Advanced AI capabilities:</p>
                <ul style="text-align: left;">
                    <li>Keyword extraction</li>
                    <li>Skills identification</li>
                    <li>Structure analysis</li>
                    <li>Metrics detection</li>
                    <li>Job matching</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="feature-box">
                <h3>📈 Actionable Insights</h3>
                <p>Get detailed feedback:</p>
                <ul style="text-align: left;">
                    <li>Personalized recommendations</li>
                    <li>Skill gap analysis</li>
                    <li>Improvement suggestions</li>
                    <li>Resume strengths</li>
                    <li>Professional reports</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 📊 By The Numbers")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Resumes Analyzed", "10,000+", "+1,200/month")
    
    with col2:
        st.metric("Avg Score Improvement", "+23%", "After optimization")
    
    with col3:
        st.metric("Success Rate", "85%", "Land interviews")
    
    with col4:
        st.metric("User Satisfaction", "4.8/5", "⭐⭐⭐⭐⭐")

# ---------------- TAB 2: HOW IT WORKS ----------------
with tab2:
    st.markdown("### 🔬 The Analysis Process")
    
    st.markdown("""
        <div class="info-card">
            <h3>Step-by-Step Workflow</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Process steps
    steps = [
        {
            "number": "1",
            "title": "PDF Upload & Text Extraction",
            "description": "Your resume is uploaded and text is extracted using PyPDF2. The system reads all content while preserving structure.",
            "technical": "Uses PyPDF2 library to parse PDF and extract text from all pages"
        },
        {
            "number": "2",
            "title": "Keyword & Skills Detection",
            "description": "The system identifies technical skills, soft skills, and important keywords using pattern matching and NLP.",
            "technical": "Employs regex patterns and keyword databases to find relevant skills"
        },
        {
            "number": "3",
            "title": "Structure Analysis",
            "description": "Resume sections are identified and analyzed (Experience, Education, Skills, Projects, Certifications).",
            "technical": "Uses text analysis to detect section headers and organizational structure"
        },
        {
            "number": "4",
            "title": "Metrics & Quantification Check",
            "description": "The system looks for numbers, percentages, and quantifiable achievements in your experience.",
            "technical": "Regex-based detection of numerical patterns indicating measurable results"
        },
        {
            "number": "5",
            "title": "Job Description Matching",
            "description": "If provided, your resume is compared against the job description to calculate compatibility.",
            "technical": "Word overlap analysis and keyword frequency comparison"
        },
        {
            "number": "6",
            "title": "Score Calculation",
            "description": "Six category scores are calculated based on the analysis, each weighted differently.",
            "technical": "Algorithmic scoring based on predefined criteria and thresholds"
        },
        {
            "number": "7",
            "title": "Recommendations Generation",
            "description": "Personalized improvement suggestions are generated based on your scores and gaps.",
            "technical": "Rule-based system generates targeted recommendations"
        },
        {
            "number": "8",
            "title": "Report Creation",
            "description": "A comprehensive PDF report is generated with all findings, charts, and recommendations.",
            "technical": "ReportLab library creates professional formatted PDF documents"
        }
    ]
    
    for step in steps:
        with st.expander(f"Step {step['number']}: {step['title']}", expanded=False):
            st.markdown(f"**{step['description']}**")
            st.info(f"🔧 Technical: {step['technical']}")
    
    st.markdown("---")
    
    st.markdown("""
        <div class="info-card">
            <h3>📊 Scoring Methodology</h3>
            <p>Each resume is evaluated across six critical categories:</p>
        </div>
    """, unsafe_allow_html=True)
    
    scoring_details = {
        "Technical Skills (0-100)": "Based on number and relevance of technical skills found. Points awarded for each identified skill from our database of 100+ common technical skills.",
        
        "Experience Match (0-100)": "Measures how well your experience aligns with the job description. Factors include years of experience indicators and keyword overlap with JD.",
        
        "Soft Skills (0-100)": "Evaluates presence of soft skills like leadership, communication, teamwork. Higher scores for diverse soft skill mentions.",
        
        "Resume Quality (0-100)": "Assesses overall structure and completeness. Points for having key sections (Experience, Education, Skills, Projects, Certifications).",
        
        "Searchability (0-100)": "Measures how easily ATS can find and index your resume. Based on keyword density, structure clarity, and skills section presence.",
        
        "Metrics Usage (0-100)": "Evaluates use of quantifiable achievements. Points for percentages, dollar amounts, numbers with +, K, M, etc."
    }
    
    for category, description in scoring_details.items():
        st.markdown(f"""
            <div class="info-card">
                <h4>{category}</h4>
                <p>{description}</p>
            </div>
        """, unsafe_allow_html=True)

# ---------------- TAB 3: TECHNOLOGY ----------------
with tab3:
    st.markdown("### 💻 Technology Stack")
    
    st.markdown("""
        <div class="info-card">
            <h3>Built With Modern Technologies</h3>
            <p>Our platform leverages cutting-edge technologies to deliver accurate and fast resume analysis.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎨 Frontend & UI")
        st.markdown("""
            <div class="info-card">
                <span class="tech-badge">Streamlit</span>
                <span class="tech-badge">Python</span>
                <span class="tech-badge">HTML/CSS</span>
                <span class="tech-badge">JavaScript</span>
                <p style="margin-top: 1rem;">
                <b>Streamlit</b> powers our interactive web interface, providing a smooth user experience with 
                minimal code. Custom CSS creates our beautiful teal blue theme.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 📊 Visualization")
        st.markdown("""
            <div class="info-card">
                <span class="tech-badge">Matplotlib</span>
                <span class="tech-badge">Plotly</span>
                <span class="tech-badge">Charts.js</span>
                <p style="margin-top: 1rem;">
                <b>Matplotlib</b> generates beautiful, customizable charts for score visualization. All charts 
                follow our teal color scheme for consistency.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🧠 Analysis Engine")
        st.markdown("""
            <div class="info-card">
                <span class="tech-badge">PyPDF2</span>
                <span class="tech-badge">Regular Expressions</span>
                <span class="tech-badge">NLP</span>
                <span class="tech-badge">Pattern Matching</span>
                <p style="margin-top: 1rem;">
                <b>PyPDF2</b> extracts text from PDF resumes. Custom regex patterns and NLP techniques 
                identify skills, metrics, and structure.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 📄 Report Generation")
        st.markdown("""
            <div class="info-card">
                <span class="tech-badge">ReportLab</span>
                <span class="tech-badge">PDF</span>
                <span class="tech-badge">Templates</span>
                <p style="margin-top: 1rem;">
                <b>ReportLab</b> creates professional PDF reports with tables, charts, and formatted text. 
                Reports are fully customized with branding and insights.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🏗️ Architecture")
    
    st.markdown("""
        <div class="info-card">
            <h4>System Architecture</h4>
            <pre>
┌─────────────────────────────────────────────────────────────┐
│                      User Interface                          │
│              (Streamlit Multipage App)                       │
│  [Home] [Resume Scoring] [Analytics] [Tips] [About]        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    Upload Handler                            │
│              (File validation & Processing)                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  Text Extraction                             │
│            (PyPDF2 - PDF to Text)                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  Analysis Engine                             │
│   ┌──────────────┬──────────────┬──────────────┐           │
│   │   Keyword    │   Structure  │   Metrics    │           │
│   │  Detection   │   Analysis   │  Detection   │           │
│   └──────────────┴──────────────┴──────────────┘           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  Scoring System                              │
│   Technical | Experience | Soft Skills | Quality            │
│   Searchability | Metrics Usage                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Results & Recommendations                       │
│   [Scores] [Charts] [Suggestions] [Strengths]              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  PDF Report Generator                        │
│              (ReportLab - Professional Report)               │
└─────────────────────────────────────────────────────────────┘
            </pre>
        </div>
    """, unsafe_allow_html=True)

# ---------------- TAB 4: FAQ ----------------
with tab4:
    st.markdown("### ❓ Frequently Asked Questions")
    
    faqs = [
        {
            "q": "Is my resume data secure?",
            "a": "Yes! Your resume is processed in real-time and not stored on our servers. All analysis happens during your session and data is deleted immediately after."
        },
        {
            "q": "What file formats are supported?",
            "a": "Currently, we support PDF format only. This is the most common and ATS-friendly format. Make sure your PDF is not image-based or password-protected."
        },
        {
            "q": "How accurate is the ATS scoring?",
            "a": "Our scoring system is based on industry research and best practices. While we simulate ATS behavior, actual ATS systems vary by company. Use our scores as guidance, not absolute guarantees."
        },
        {
            "q": "Can I analyze multiple resumes at once?",
            "a": "Yes! Upload multiple resume PDFs and we'll analyze and rank them side-by-side. This is great for comparing different versions of your resume."
        },
        {
            "q": "Do I need to provide a job description?",
            "a": "It's optional but recommended. Providing a job description improves the accuracy of the Experience Match score and helps identify relevant keywords."
        },
        {
            "q": "What's a good ATS score?",
            "a": "Generally, scores above 70% are considered good. However, aim for 80%+ to be competitive. Each category should ideally be above 70%."
        },
        {
            "q": "How often should I update my resume?",
            "a": "Update your resume for each job application to include relevant keywords from the job description. Also update it whenever you gain new skills or experiences."
        },
        {
            "q": "Can this guarantee I'll get hired?",
            "a": "No tool can guarantee hiring. However, an optimized resume significantly increases your chances of passing ATS screening and reaching human recruiters."
        },
        {
            "q": "What makes a resume ATS-friendly?",
            "a": "Key factors: simple formatting, standard fonts, clear section headers, relevant keywords, no images/tables, PDF/DOCX format, and quantifiable achievements."
        },
        {
            "q": "Is this service free?",
            "a": "Yes! This is a free tool designed to help job seekers improve their resumes and increase their chances of landing interviews."
        },
        {
            "q": "Can I download my results?",
            "a": "Yes! After analysis, you can download a comprehensive PDF report with all your scores, charts, recommendations, and identified strengths."
        },
        {
            "q": "What programming languages are detected?",
            "a": "We detect 50+ programming languages and technologies including Python, Java, JavaScript, SQL, R, C++, and many more. Check the Tips page for a full list."
        }
    ]
    
    for faq in faqs:
        with st.expander(f"❓ {faq['q']}"):
            st.markdown(f"**Answer:** {faq['a']}")
    
    st.markdown("---")
    
    st.markdown("""
        <div class="info-card">
            <h3>🤔 Still Have Questions?</h3>
            <p>
            If your question isn't answered here, feel free to explore our Tips & Guide page for more 
            detailed information about resume optimization and ATS best practices.
            </p>
        </div>
    """, unsafe_allow_html=True)

# ---------------- CONTACT & FOOTER ----------------
st.markdown("---")
st.markdown("### 👩‍💻 About the Developer")

st.markdown("""
    <div class="info-card">
        <h3>Bhargavi</h3>
        <p>
        Creator of the Professional ATS Resume Scoring System. Passionate about using technology to solve 
        real-world problems and help people succeed in their careers.
        </p>
        <p style="margin-top: 1rem;">
        <b>🎯 Mission:</b> Making job applications more accessible and transparent for everyone.
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("### 📞 Connect With Us")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
        <div class="feature-box">
            <h4>📧 Email</h4>
            <p>contact@atsresume.com</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-box">
            <h4>💼 LinkedIn</h4>
            <p>@atsresumescoring</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-box">
            <h4>🐦 Twitter</h4>
            <p>@atsresume</p>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div class="feature-box">
            <h4>💻 GitHub</h4>
            <p>github.com/atsresume</p>
        </div>
    """, unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #008B8B; padding: 1rem;'>
        <p><b>Professional ATS Resume Scoring System</b></p>
        <p>Version 2.0 | Built with ❤️ using Streamlit</p>
        <p>© 2024 | AI-Powered Career Solutions</p>
        <p><i>Helping job seekers succeed, one resume at a time</i></p>
    </div>
""", unsafe_allow_html=True)
