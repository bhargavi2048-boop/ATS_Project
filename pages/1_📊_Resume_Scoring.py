import streamlit as st
import matplotlib.pyplot as plt
import PyPDF2
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
import datetime
import re

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Resume Scoring | ATS System", page_icon="📊", layout="wide")

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
    
    .score-card {
        background: linear-gradient(135deg, #E0FFFF 0%, #AFEEEE 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #008B8B;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 139, 139, 0.2);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #008B8B 0%, #20B2AA 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #006666 0%, #008B8B 100%);
        box-shadow: 0 4px 8px rgba(0, 139, 139, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- FUNCTIONS ----------------

def extract_text(pdf_file):
    """Extracts text from a PDF file."""
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text.lower()
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
        return ""

def extract_keywords(text):
    """Extract important keywords from resume text."""
    # Technical skills keywords
    technical_keywords = [
        'python', 'java', 'javascript', 'sql', 'react', 'angular', 'node.js',
        'aws', 'azure', 'docker', 'kubernetes', 'git', 'machine learning',
        'data analysis', 'tableau', 'power bi', 'excel', 'r programming',
        'tensorflow', 'pytorch', 'pandas', 'numpy', 'scikit-learn'
    ]
    
    # Soft skills keywords
    soft_skills = [
        'leadership', 'communication', 'teamwork', 'problem solving',
        'analytical', 'creative', 'adaptable', 'organized', 'detail-oriented',
        'collaborative', 'innovative', 'strategic'
    ]
    
    found_technical = [kw for kw in technical_keywords if kw in text.lower()]
    found_soft = [kw for kw in soft_skills if kw in text.lower()]
    
    return found_technical, found_soft

def count_metrics(text):
    """Count usage of quantifiable metrics in resume."""
    # Look for numbers followed by common metric indicators
    patterns = [
        r'\d+%',  # Percentages
        r'\$\d+',  # Dollar amounts
        r'\d+\+',  # Numbers with plus
        r'\d+k',  # Thousands
        r'\d+m',  # Millions
    ]
    
    metrics_count = 0
    for pattern in patterns:
        metrics_count += len(re.findall(pattern, text.lower()))
    
    return metrics_count

def analyze_resume_structure(text):
    """Analyze resume structure and sections."""
    sections = {
        'Experience': False,
        'Education': False,
        'Skills': False,
        'Projects': False,
        'Certifications': False
    }
    
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['experience', 'work history', 'employment']):
        sections['Experience'] = True
    if any(word in text_lower for word in ['education', 'academic', 'degree']):
        sections['Education'] = True
    if any(word in text_lower for word in ['skills', 'technical skills', 'competencies']):
        sections['Skills'] = True
    if any(word in text_lower for word in ['projects', 'portfolio']):
        sections['Projects'] = True
    if any(word in text_lower for word in ['certification', 'certified', 'licenses']):
        sections['Certifications'] = True
    
    return sections

def calculate_scores(resume_text, job_description):
    """Calculate detailed ATS scores based on resume content."""
    scores = {}
    
    # Extract keywords
    tech_skills, soft_skills = extract_keywords(resume_text)
    
    # Technical Skills Score (0-100)
    tech_score = min(len(tech_skills) * 10, 100)
    scores['Technical Skills'] = tech_score
    
    # Experience Match Score (0-100)
    # Check for years of experience
    exp_match = 50  # Base score
    if 'years' in resume_text or 'year' in resume_text:
        exp_match += 20
    if job_description:
        # Simple keyword matching with job description
        jd_words = set(job_description.lower().split())
        resume_words = set(resume_text.split())
        common_words = jd_words.intersection(resume_words)
        exp_match += min(len(common_words) * 2, 30)
    scores['Experience Match'] = min(exp_match, 100)
    
    # Soft Skills Score (0-100)
    soft_score = min(len(soft_skills) * 15, 100)
    scores['Soft Skills'] = max(soft_score, 50)  # Minimum 50
    
    # Resume Quality Score (0-100)
    quality_score = 60  # Base score
    sections = analyze_resume_structure(resume_text)
    quality_score += sum(10 for present in sections.values() if present)
    scores['Resume Quality'] = min(quality_score, 100)
    
    # Searchability Score (0-100)
    # Based on structure and keywords
    searchability = 70  # Base score
    if sections['Skills']:
        searchability += 15
    if len(tech_skills) > 5:
        searchability += 15
    scores['Searchability'] = min(searchability, 100)
    
    # Metrics Usage Score (0-100)
    metrics_count = count_metrics(resume_text)
    metrics_score = min(metrics_count * 20, 100)
    scores['Metrics Usage'] = max(metrics_score, 30)  # Minimum 30
    
    return scores, tech_skills, soft_skills

def generate_improvement_suggestions(scores, tech_skills, sections):
    """Generate personalized improvement suggestions."""
    suggestions = []
    
    if scores['Technical Skills'] < 70:
        suggestions.append("🔧 Add more technical skills relevant to your target role (SQL, Python, Excel, etc.)")
    
    if scores['Experience Match'] < 70:
        suggestions.append("📝 Align your experience section more closely with job description keywords")
    
    if scores['Metrics Usage'] < 70:
        suggestions.append("📊 Add quantifiable achievements using numbers, percentages, and metrics")
    
    if not sections.get('Projects', False):
        suggestions.append("💼 Include a Projects section to showcase practical application of skills")
    
    if scores['Searchability'] < 80:
        suggestions.append("🔍 Use more industry-standard keywords to improve ATS searchability")
    
    if scores['Soft Skills'] < 70:
        suggestions.append("🤝 Highlight soft skills like leadership, communication, and teamwork")
    
    if len(tech_skills) < 5:
        suggestions.append("⚙️ Expand your skills section with tools and technologies you've used")
    
    # Always include best practices
    suggestions.append("✨ Use strong action verbs (Led, Developed, Implemented, Achieved)")
    suggestions.append("📄 Keep formatting clean and ATS-friendly (avoid images, tables, columns)")
    suggestions.append("🎯 Tailor your resume for each specific job application")
    
    return suggestions

def generate_resume_strengths(scores, sections):
    """Identify resume strengths."""
    strengths = []
    
    if scores['Technical Skills'] >= 70:
        strengths.append("✅ Strong technical skills portfolio")
    
    if scores['Experience Match'] >= 70:
        strengths.append("✅ Good alignment with job requirements")
    
    if scores['Resume Quality'] >= 80:
        strengths.append("✅ Well-structured resume with clear sections")
    
    if scores['Searchability'] >= 80:
        strengths.append("✅ High ATS searchability with good keyword usage")
    
    if scores['Metrics Usage'] >= 70:
        strengths.append("✅ Excellent use of quantifiable achievements")
    
    if sections.get('Certifications', False):
        strengths.append("✅ Professional certifications demonstrate commitment")
    
    if sections.get('Projects', False):
        strengths.append("✅ Project experience shows practical skills")
    
    # Always include at least some positive feedback
    if len(strengths) == 0:
        strengths.append("✅ Resume has potential for significant improvement")
    
    return strengths

def create_pdf_report(resumes_data):
    """Generates a professional PDF report for multiple resumes."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph("<b>ATS Resume Evaluation Report</b>", styles["Title"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(
        f"Generated on: {datetime.datetime.now().strftime('%d %B %Y, %I:%M %p')}", 
        styles["Normal"]
    ))
    elements.append(Spacer(1, 20))

    for idx, data in enumerate(resumes_data, 1):
        # Resume header
        elements.append(Paragraph(
            f"<b>Resume #{idx}: {data['name']}</b>", 
            styles["Heading2"]
        ))
        elements.append(Paragraph(f"Target Role: {data['role']}", styles["Normal"]))
        elements.append(Paragraph(
            f"Overall ATS Score: <b><font color='{TEAL_DARK}'>{data['overall_score']}%</font></b>", 
            styles["Normal"]
        ))
        elements.append(Spacer(1, 12))

        # Score breakdown table
        table_data = [["Category", "Score (%)", "Status"]]
        for category, score in data['scores'].items():
            status = "✓ Good" if score >= 70 else "⚠ Needs Work"
            table_data.append([category, f"{score:.1f}", status])
        
        table = Table(table_data, colWidths=[200, 80, 100])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(TEAL_PRIMARY)),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#E0FFFF")),
            ("GRID", (0, 0), (-1, -1), 1, colors.HexColor(TEAL_DARK)),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))

        # Keywords found
        if data.get('tech_skills'):
            elements.append(Paragraph("<b>Technical Skills Found:</b>", styles["Heading3"]))
            elements.append(Paragraph(", ".join(data['tech_skills'][:10]), styles["Normal"]))
            elements.append(Spacer(1, 8))

        # Improvement recommendations
        elements.append(Paragraph("<b>Improvement Recommendations:</b>", styles["Heading3"]))
        for tip in data['improvements']:
            elements.append(Paragraph(f"• {tip}", styles["Normal"]))
            elements.append(Spacer(1, 4))
        elements.append(Spacer(1, 8))

        # Strengths
        elements.append(Paragraph("<b>Resume Strengths:</b>", styles["Heading3"]))
        for strength in data['strengths']:
            elements.append(Paragraph(f"• {strength}", styles["Normal"]))
            elements.append(Spacer(1, 4))

        elements.append(Spacer(1, 30))

    # Footer
    elements.append(Paragraph(
        "<i>Generated by Professional ATS Resume Scoring System | AI-Powered Career Solutions</i>", 
        styles["Normal"]
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer

# ---------------- HEADER ----------------
st.markdown("""
    <div class="main-header">
        <h1>📊 Resume Scoring & Analysis</h1>
        <p>Upload your resume and get instant ATS compatibility scores</p>
    </div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.info("Configure your analysis settings here")

# ---------------- INPUT SECTION ----------------
st.markdown("### 📋 Step 1: Job Information")

col1, col2 = st.columns([1, 1])

with col1:
    job_role = st.selectbox(
        "Select Target Job Role *",
        ["", "Data Analyst", "Data Scientist", "Software Engineer", "Web Developer", 
         "Business Analyst", "Product Manager", "DevOps Engineer", "UI/UX Designer",
         "Machine Learning Engineer", "Full Stack Developer"],
        help="Select the job role you're applying for"
    )

with col2:
    experience_level = st.selectbox(
        "Experience Level",
        ["Entry Level", "Mid Level", "Senior Level", "Lead/Manager"],
        help="Your experience level"
    )

st.markdown("### 📝 Step 2: Job Description (Optional)")
jd = st.text_area(
    "Paste Job Description",
    height=150,
    placeholder="Paste the job description here to get more accurate matching scores...",
    help="Adding a job description improves the accuracy of experience matching"
)

st.markdown("### 📄 Step 3: Upload Resume(s)")
uploaded_files = st.file_uploader(
    "Upload Resume PDFs",
    type=["pdf"],
    accept_multiple_files=True,
    help="You can upload multiple resumes to compare them"
)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} resume(s) uploaded successfully!")

# ---------------- ANALYSIS SECTION ----------------
st.markdown("### 🚀 Step 4: Run Analysis")

if st.button("🎯 Analyze Resume(s)", use_container_width=True):
    if not uploaded_files:
        st.error("❌ Please upload at least one PDF resume file.")
    elif not job_role:
        st.error("❌ Please select a job role.")
    else:
        with st.spinner("🔍 Analyzing resumes... Please wait..."):
            resumes_data = []
            
            for file in uploaded_files:
                # Extract text
                resume_text = extract_text(file)
                
                if not resume_text:
                    st.warning(f"⚠️ Could not extract text from {file.name}")
                    continue
                
                # Calculate scores
                scores, tech_skills, soft_skills = calculate_scores(resume_text, jd)
                overall_score = round(sum(scores.values()) / len(scores), 2)
                
                # Analyze structure
                sections = analyze_resume_structure(resume_text)
                
                # Generate suggestions
                improvements = generate_improvement_suggestions(scores, tech_skills, sections)
                strengths = generate_resume_strengths(scores, sections)
                
                resumes_data.append({
                    "name": file.name,
                    "role": job_role,
                    "scores": scores,
                    "overall_score": overall_score,
                    "improvements": improvements,
                    "strengths": strengths,
                    "tech_skills": tech_skills,
                    "soft_skills": soft_skills,
                    "sections": sections
                })

            if not resumes_data:
                st.error("❌ Could not analyze any of the uploaded resumes.")
            else:
                # Sort resumes by score (descending)
                resumes_data = sorted(resumes_data, key=lambda x: x['overall_score'], reverse=True)

                st.markdown("---")
                st.markdown("## 🏆 Analysis Results")

                # Show ranking if multiple resumes
                if len(resumes_data) > 1:
                    st.markdown("### 📊 Resume Ranking")
                    rank_df_data = []
                    for idx, r in enumerate(resumes_data, 1):
                        rank_df_data.append({
                            "Rank": f"#{idx}",
                            "Resume": r['name'],
                            "Overall Score": f"{r['overall_score']}%",
                            "Status": "✅ Strong" if r['overall_score'] >= 70 else "⚠️ Needs Work"
                        })
                    
                    st.dataframe(rank_df_data, use_container_width=True)
                    st.markdown("---")

                # Detailed results for each resume
                for idx, r in enumerate(resumes_data, 1):
                    with st.expander(f"📄 {r['name']} - Overall Score: {r['overall_score']}%", expanded=(idx == 1)):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            # Score breakdown chart
                            fig, ax = plt.subplots(figsize=(10, 5))
                            categories = list(r['scores'].keys())
                            values = list(r['scores'].values())
                            colors_bars = [TEAL_PRIMARY if v >= 70 else TEAL_SECONDARY for v in values]
                            
                            bars = ax.barh(categories, values, color=colors_bars)
                            ax.set_xlim(0, 100)
                            ax.set_xlabel('Score (%)', fontweight='bold', color=TEAL_DARK)
                            ax.set_title(f'ATS Score Breakdown - {r["name"]}', 
                                       fontsize=14, fontweight='bold', color=TEAL_DARK)
                            ax.axvline(x=70, color='red', linestyle='--', linewidth=1, alpha=0.5)
                            ax.text(71, len(categories)-0.5, 'Target: 70%', color='red', fontsize=9)
                            
                            # Add value labels on bars
                            for i, (bar, value) in enumerate(zip(bars, values)):
                                ax.text(value + 2, i, f'{value:.1f}%', 
                                       va='center', fontweight='bold', color=TEAL_DARK)
                            
                            ax.grid(axis='x', alpha=0.3)
                            plt.tight_layout()
                            st.pyplot(fig)
                            plt.close()
                        
                        with col2:
                            # Overall score display
                            st.markdown(f"""
                                <div class="score-card">
                                    <h2 style="text-align: center; color: {TEAL_DARK};">
                                        {r['overall_score']}%
                                    </h2>
                                    <p style="text-align: center; color: {TEAL_PRIMARY};">
                                        <b>Overall ATS Score</b>
                                    </p>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            # Key metrics
                            st.metric("Technical Skills Found", len(r['tech_skills']))
                            st.metric("Soft Skills Found", len(r['soft_skills']))
                            st.metric("Resume Sections", 
                                    f"{sum(r['sections'].values())}/5")

                        # Keywords found
                        if r['tech_skills']:
                            st.markdown("#### 🔧 Technical Skills Detected")
                            st.info(", ".join(r['tech_skills'][:15]))
                        
                        if r['soft_skills']:
                            st.markdown("#### 🤝 Soft Skills Detected")
                            st.info(", ".join(r['soft_skills'][:10]))

                        # Resume sections
                        st.markdown("#### 📋 Resume Structure Analysis")
                        section_cols = st.columns(5)
                        for idx, (section, present) in enumerate(r['sections'].items()):
                            with section_cols[idx]:
                                if present:
                                    st.success(f"✅ {section}")
                                else:
                                    st.error(f"❌ {section}")

                        # Improvements
                        st.markdown("#### 💡 Improvement Recommendations")
                        for tip in r['improvements']:
                            st.warning(tip)

                        # Strengths
                        st.markdown("#### ✨ Resume Strengths")
                        for strength in r['strengths']:
                            st.success(strength)

                st.markdown("---")

                # PDF Download
                st.markdown("### 📥 Download Professional Report")
                pdf = create_pdf_report(resumes_data)
                st.download_button(
                    label="📄 Download Detailed PDF Report",
                    data=pdf,
                    file_name=f"ATS_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #008B8B;'>
        <p><i>💡 Tip: Upload multiple resumes to compare and rank them side by side</i></p>
    </div>
""", unsafe_allow_html=True)
