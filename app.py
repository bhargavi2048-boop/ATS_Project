import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="ATS Resume Scoring System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS FOR TEAL BLUE THEME ----------------
st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --teal-primary: #008B8B;
        --teal-secondary: #20B2AA;
        --teal-dark: #006666;
        --teal-light: #AFEEEE;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #008B8B 0%, #20B2AA 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 139, 139, 0.3);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        color: #E0FFFF;
        font-size: 1.2rem;
    }
    
    /* Feature cards */
    .feature-card {
        background: linear-gradient(135deg, #E0FFFF 0%, #AFEEEE 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #008B8B;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 139, 139, 0.2);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0, 139, 139, 0.3);
    }
    
    .feature-card h3 {
        color: #006666;
        margin-bottom: 0.5rem;
    }
    
    .feature-card p {
        color: #008B8B;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #008B8B 0%, #20B2AA 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #006666 0%, #008B8B 100%);
        box-shadow: 0 4px 8px rgba(0, 139, 139, 0.4);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #E0FFFF 0%, #AFEEEE 100%);
    }
    
    /* Info boxes */
    .stAlert {
        background-color: #E0FFFF;
        border-left: 5px solid #008B8B;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        color: #008B8B;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
    <div class="main-header">
        <h1>📄 Professional ATS Resume Scoring System</h1>
        <p>AI-Powered Resume Analysis & Optimization Platform</p>
    </div>
""", unsafe_allow_html=True)

# ---------------- WELCOME SECTION ----------------
st.markdown("### 🎯 Welcome to Your Career Success Partner")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="feature-card">
            <h3>🚀 What We Offer</h3>
            <p>
            Our advanced ATS (Applicant Tracking System) uses cutting-edge AI and Natural Language Processing 
            to evaluate your resume against job descriptions. Get instant feedback, detailed insights, 
            and actionable recommendations to improve your chances of landing your dream job.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
with col2:
    st.markdown("""
        <div class="feature-card">
            <h3>💡 Why Choose Us?</h3>
            <p>
            • Comprehensive resume analysis<br>
            • Multi-resume comparison<br>
            • Real-time ATS scoring<br>
            • Professional PDF reports<br>
            • Expert improvement tips
            </p>
        </div>
    """, unsafe_allow_html=True)

# ---------------- KEY FEATURES ----------------
st.markdown("### ✨ Key Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="feature-card">
            <h3>📊 Resume Scoring</h3>
            <p>Upload your resume and get detailed ATS compatibility scores across multiple categories including technical skills, experience match, and formatting quality.</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <h3>📈 Analytics Dashboard</h3>
            <p>View comprehensive analytics and visualizations of your resume performance. Compare multiple resumes and identify areas for improvement.</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-card">
            <h3>💡 Expert Tips & Guides</h3>
            <p>Access our comprehensive library of resume writing tips, best practices, and industry-specific guidance to create ATS-friendly resumes.</p>
        </div>
    """, unsafe_allow_html=True)

# ---------------- HOW IT WORKS ----------------
st.markdown("### 🔄 How It Works")

st.markdown("""
    <div class="feature-card">
        <h3>Simple 4-Step Process</h3>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("#### 1️⃣ Select Role")
    st.info("Choose your target job role from our predefined list")

with col2:
    st.markdown("#### 2️⃣ Upload Resume")
    st.info("Upload one or multiple PDF resumes for analysis")

with col3:
    st.markdown("#### 3️⃣ Get Analysis")
    st.info("Receive detailed ATS scores and insights instantly")

with col4:
    st.markdown("#### 4️⃣ Improve")
    st.info("Follow recommendations to optimize your resume")

# ---------------- QUICK STATS ----------------
st.markdown("### 📊 Quick Stats")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Success Rate", value="85%", delta="↑ 12%")

with col2:
    st.metric(label="Avg Score Improvement", value="+23%", delta="↑ 5%")

with col3:
    st.metric(label="Resumes Analyzed", value="10K+", delta="Growing")

with col4:
    st.metric(label="Job Roles Supported", value="50+", delta="Expanding")

# ---------------- GETTING STARTED ----------------
st.markdown("### 🎯 Getting Started")

st.info("""
    👈 **Navigate using the sidebar** to access different features:
    - **📊 Resume Scoring**: Upload and analyze your resumes
    - **📈 Analytics**: View detailed performance analytics
    - **💡 Tips & Guide**: Learn best practices for resume writing
    - **ℹ️ About**: Learn more about the system and how it works
""")

# ---------------- TESTIMONIALS ----------------
st.markdown("### 💬 What Our Users Say")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="feature-card">
            <p><i>"This tool helped me optimize my resume and I landed 3 interviews within a week!"</i></p>
            <p><b>- Sarah M., Data Analyst</b></p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <p><i>"The detailed feedback and scoring system gave me clear direction on what to improve."</i></p>
            <p><b>- John D., Software Engineer</b></p>
        </div>
    """, unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #008B8B; padding: 1rem;'>
        <p><b>Professional ATS Resume Scoring System</b></p>
        <p>© 2024 | AI-Powered Career Solutions | Made with ❤️ by Bhargavi</p>
    </div>
""", unsafe_allow_html=True)
