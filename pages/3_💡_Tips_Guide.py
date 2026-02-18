import streamlit as st

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Tips & Guide | ATS System", page_icon="💡", layout="wide")

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
    
    .tip-card {
        background: linear-gradient(135deg, #E0FFFF 0%, #AFEEEE 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #008B8B;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 139, 139, 0.2);
    }
    
    .tip-card h3 {
        color: #006666;
        margin-bottom: 1rem;
    }
    
    .tip-card h4 {
        color: #008B8B;
        margin-top: 1rem;
    }
    
    .do-card {
        background: #D4EDDA;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28A745;
        margin: 0.5rem 0;
    }
    
    .dont-card {
        background: #F8D7DA;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #DC3545;
        margin: 0.5rem 0;
    }
    
    .example-good {
        background: #E8F5E9;
        padding: 1rem;
        border-radius: 5px;
        font-family: monospace;
        border-left: 3px solid #4CAF50;
    }
    
    .example-bad {
        background: #FFEBEE;
        padding: 1rem;
        border-radius: 5px;
        font-family: monospace;
        border-left: 3px solid #F44336;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
    <div class="main-header">
        <h1>💡 Resume Tips & Best Practices Guide</h1>
        <p>Expert advice to create ATS-friendly resumes that get noticed</p>
    </div>
""", unsafe_allow_html=True)

# ---------------- NAVIGATION TABS ----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📝 General Tips",
    "🔧 Technical Skills",
    "📊 Formatting",
    "🎯 Keywords",
    "📋 Examples"
])

# ---------------- TAB 1: GENERAL TIPS ----------------
with tab1:
    st.markdown("### 📝 Essential Resume Writing Tips")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="tip-card">
                <h3>✅ Do's</h3>
                <ul>
                    <li><b>Keep it concise:</b> 1-2 pages maximum</li>
                    <li><b>Use action verbs:</b> Led, Developed, Implemented, Achieved</li>
                    <li><b>Quantify achievements:</b> Include numbers, percentages, metrics</li>
                    <li><b>Tailor for each job:</b> Customize for specific roles</li>
                    <li><b>Include relevant keywords:</b> Match job description</li>
                    <li><b>Use clear headings:</b> Experience, Education, Skills</li>
                    <li><b>List recent experience first:</b> Reverse chronological order</li>
                    <li><b>Proofread carefully:</b> Zero typos and grammar errors</li>
                    <li><b>Use standard fonts:</b> Arial, Calibri, Times New Roman</li>
                    <li><b>Save as PDF:</b> Preserve formatting across systems</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="tip-card">
                <h3>❌ Don'ts</h3>
                <ul>
                    <li><b>Don't use images or photos:</b> ATS can't read them</li>
                    <li><b>Don't use tables or columns:</b> Causes parsing issues</li>
                    <li><b>Don't use headers/footers:</b> Content may be lost</li>
                    <li><b>Don't include personal info:</b> Age, marital status, photo</li>
                    <li><b>Don't use fancy fonts:</b> Stick to standard, readable fonts</li>
                    <li><b>Don't use abbreviations:</b> Spell out acronyms first</li>
                    <li><b>Don't lie or exaggerate:</b> Be honest about skills</li>
                    <li><b>Don't use "I" or "me":</b> Use third person or implied subject</li>
                    <li><b>Don't list duties:</b> Focus on achievements instead</li>
                    <li><b>Don't use templates:</b> They may not be ATS-friendly</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
        <div class="tip-card">
            <h3>🎯 Key Sections Every Resume Must Have</h3>
            <h4>1. Contact Information</h4>
            <p>Name, Phone, Email, LinkedIn, Location (City, State)</p>
            
            <h4>2. Professional Summary/Objective</h4>
            <p>2-3 sentences highlighting your experience and career goals</p>
            
            <h4>3. Work Experience</h4>
            <p>Job title, Company, Dates, Achievements (with metrics)</p>
            
            <h4>4. Education</h4>
            <p>Degree, Institution, Graduation year, GPA (if recent & high)</p>
            
            <h4>5. Skills</h4>
            <p>Technical skills, Tools, Certifications, Languages</p>
            
            <h4>6. Additional Sections (Optional but Recommended)</h4>
            <ul>
                <li>Projects (especially for tech roles)</li>
                <li>Certifications (professional credentials)</li>
                <li>Awards & Achievements</li>
                <li>Publications (for research roles)</li>
                <li>Volunteer Experience</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# ---------------- TAB 2: TECHNICAL SKILLS ----------------
with tab2:
    st.markdown("### 🔧 Technical Skills Best Practices")
    
    st.markdown("""
        <div class="tip-card">
            <h3>How to List Technical Skills</h3>
            <p>Organize your skills into clear categories for easy scanning:</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ✅ Good Example")
        st.markdown("""
            <div class="example-good">
            <b>TECHNICAL SKILLS</b><br><br>
            <b>Programming Languages:</b> Python, Java, SQL, R<br>
            <b>Data Analysis:</b> Pandas, NumPy, SciPy, Excel<br>
            <b>Visualization:</b> Tableau, Power BI, Matplotlib<br>
            <b>Database:</b> MySQL, PostgreSQL, MongoDB<br>
            <b>Cloud:</b> AWS (S3, EC2), Azure<br>
            <b>Tools:</b> Git, Docker, Jupyter, VS Code
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### ❌ Bad Example")
        st.markdown("""
            <div class="example-bad">
            <b>SKILLS</b><br><br>
            Python, Excel, Communication, Leadership,
            Problem Solving, Microsoft Word, Email,
            Typing, Internet, Windows, Teamwork,
            Hardworking, Quick Learner
            </div>
        """, unsafe_allow_html=True)
        st.caption("⚠️ Issues: Mixes technical & soft skills, includes basic skills, not organized")
    
    st.markdown("---")
    
    st.markdown("""
        <div class="tip-card">
            <h3>💼 Most In-Demand Technical Skills by Role</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="tip-card">
                <h4>📊 Data Analyst</h4>
                <ul>
                    <li>SQL ⭐⭐⭐⭐⭐</li>
                    <li>Excel ⭐⭐⭐⭐⭐</li>
                    <li>Python/R ⭐⭐⭐⭐</li>
                    <li>Tableau/Power BI ⭐⭐⭐⭐</li>
                    <li>Statistics ⭐⭐⭐⭐</li>
                    <li>Data Visualization ⭐⭐⭐</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="tip-card">
                <h4>💻 Software Engineer</h4>
                <ul>
                    <li>Programming (Java/Python) ⭐⭐⭐⭐⭐</li>
                    <li>Data Structures ⭐⭐⭐⭐⭐</li>
                    <li>Git/Version Control ⭐⭐⭐⭐</li>
                    <li>APIs/REST ⭐⭐⭐⭐</li>
                    <li>Testing ⭐⭐⭐⭐</li>
                    <li>Cloud (AWS/Azure) ⭐⭐⭐</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="tip-card">
                <h4>🔬 Data Scientist</h4>
                <ul>
                    <li>Machine Learning ⭐⭐⭐⭐⭐</li>
                    <li>Python ⭐⭐⭐⭐⭐</li>
                    <li>Statistics ⭐⭐⭐⭐⭐</li>
                    <li>SQL ⭐⭐⭐⭐</li>
                    <li>Deep Learning ⭐⭐⭐⭐</li>
                    <li>Big Data (Spark) ⭐⭐⭐</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

# ---------------- TAB 3: FORMATTING ----------------
with tab3:
    st.markdown("### 📊 ATS-Friendly Formatting Guidelines")
    
    st.markdown("""
        <div class="tip-card">
            <h3>📄 Document Format & Structure</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="do-card">
                <h4>✅ ATS-Friendly Formats</h4>
                <ul>
                    <li><b>File Type:</b> .PDF or .DOCX</li>
                    <li><b>Font:</b> Arial, Calibri, Helvetica, Times New Roman</li>
                    <li><b>Font Size:</b> 10-12pt for body, 14-16pt for name</li>
                    <li><b>Margins:</b> 0.5" to 1" on all sides</li>
                    <li><b>Line Spacing:</b> 1.0 to 1.15</li>
                    <li><b>Alignment:</b> Left-aligned text</li>
                    <li><b>Bullets:</b> Standard bullets (•, -, or ►)</li>
                    <li><b>Section Headers:</b> Bold, slightly larger font</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="dont-card">
                <h4>❌ ATS-Unfriendly Elements</h4>
                <ul>
                    <li><b>Text Boxes:</b> Content may not be parsed</li>
                    <li><b>Tables:</b> Can confuse ATS systems</li>
                    <li><b>Images/Graphics:</b> Cannot be read</li>
                    <li><b>Headers/Footers:</b> Often ignored by ATS</li>
                    <li><b>Columns:</b> May be read in wrong order</li>
                    <li><b>Special Characters:</b> Can cause errors</li>
                    <li><b>Fancy Fonts:</b> May not render correctly</li>
                    <li><b>Charts/Graphs:</b> Cannot be interpreted</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
        <div class="tip-card">
            <h3>✨ Visual Hierarchy Tips</h3>
            <ol>
                <li><b>Name:</b> Largest, bold, at the top</li>
                <li><b>Section Headers:</b> Bold, uppercase or slightly larger</li>
                <li><b>Job Titles:</b> Bold, followed by company name</li>
                <li><b>Dates:</b> Right-aligned or after company name</li>
                <li><b>Bullet Points:</b> For achievements and responsibilities</li>
                <li><b>White Space:</b> Use spacing between sections</li>
            </ol>
        </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 **Pro Tip:** Test your resume by copying and pasting it into a plain text editor. If it's still readable, it's ATS-friendly!")

# ---------------- TAB 4: KEYWORDS ----------------
with tab4:
    st.markdown("### 🎯 Strategic Keyword Optimization")
    
    st.markdown("""
        <div class="tip-card">
            <h3>🔍 How to Find the Right Keywords</h3>
            <ol>
                <li><b>Analyze Job Description:</b> Highlight technical skills, tools, and qualifications</li>
                <li><b>Look for Repetition:</b> Skills mentioned multiple times are most important</li>
                <li><b>Check "Required" vs "Preferred":</b> Prioritize required skills</li>
                <li><b>Note Specific Tools:</b> Include exact names (e.g., "Tableau" not just "visualization")</li>
                <li><b>Include Certifications:</b> If mentioned, add them to your resume</li>
            </ol>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="tip-card">
                <h3>🔑 Types of Keywords to Include</h3>
                <h4>1. Hard Skills</h4>
                <ul>
                    <li>Programming languages</li>
                    <li>Software and tools</li>
                    <li>Technical processes</li>
                    <li>Certifications</li>
                </ul>
                
                <h4>2. Soft Skills</h4>
                <ul>
                    <li>Leadership</li>
                    <li>Communication</li>
                    <li>Problem-solving</li>
                    <li>Teamwork</li>
                </ul>
                
                <h4>3. Action Verbs</h4>
                <ul>
                    <li>Achieved, Developed</li>
                    <li>Implemented, Led</li>
                    <li>Optimized, Increased</li>
                    <li>Streamlined, Transformed</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="tip-card">
                <h3>📊 Where to Place Keywords</h3>
                <h4>1. Professional Summary</h4>
                <p>Include 3-5 most important keywords</p>
                
                <h4>2. Skills Section</h4>
                <p>List all relevant technical skills</p>
                
                <h4>3. Work Experience</h4>
                <p>Naturally incorporate in achievements</p>
                
                <h4>4. Project Descriptions</h4>
                <p>Mention tools and technologies used</p>
                
                <h4>5. Education & Certifications</h4>
                <p>Include relevant coursework and certs</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.warning("""
        ⚠️ **Important:** Don't keyword stuff! Use keywords naturally in context. 
        ATS systems are sophisticated and can detect artificial keyword loading.
    """)
    
    st.markdown("""
        <div class="tip-card">
            <h3>📝 Keyword Example: Data Analyst Position</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### ✅ Natural Keyword Integration")
    st.markdown("""
        <div class="example-good">
        <b>Data Analyst</b> | ABC Company | Jan 2022 - Present<br><br>
        • Developed <b>Python</b> scripts using <b>Pandas</b> and <b>NumPy</b> to automate data cleaning, 
        reducing processing time by 40%<br>
        • Created interactive dashboards in <b>Tableau</b> and <b>Power BI</b> for executive reporting, 
        improving decision-making efficiency by 25%<br>
        • Performed <b>SQL</b> queries on <b>PostgreSQL</b> database to extract insights from 2M+ records<br>
        • Conducted <b>statistical analysis</b> using <b>R</b> to identify trends and patterns in customer behavior
        </div>
    """, unsafe_allow_html=True)
    
    st.caption("✅ Keywords integrated naturally with quantified achievements")

# ---------------- TAB 5: EXAMPLES ----------------
with tab5:
    st.markdown("### 📋 Resume Examples & Templates")
    
    st.markdown("""
        <div class="tip-card">
            <h3>📝 Sample Resume Sections</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Professional Summary Examples
    st.markdown("#### 💼 Professional Summary Examples")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Entry Level - Data Analyst**")
        st.markdown("""
            <div class="example-good">
            Recent graduate with Bachelor's in Statistics and strong analytical skills. 
            Proficient in SQL, Python, and Tableau with hands-on experience through 
            academic projects and internships. Passionate about transforming data into 
            actionable insights to drive business decisions.
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Experienced - Software Engineer**")
        st.markdown("""
            <div class="example-good">
            Results-driven Software Engineer with 5+ years of experience developing 
            scalable web applications using Java, React, and AWS. Proven track record 
            of delivering projects 20% ahead of schedule while maintaining 99.9% uptime. 
            Strong expertise in microservices architecture and agile methodologies.
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Work Experience Examples
    st.markdown("#### 💼 Work Experience Examples")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ❌ Weak (Job Duties)")
        st.markdown("""
            <div class="example-bad">
            <b>Data Analyst | XYZ Corp | 2021-2023</b><br><br>
            • Responsible for analyzing data<br>
            • Created reports for management<br>
            • Used SQL and Excel<br>
            • Worked with team members<br>
            • Attended meetings
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### ✅ Strong (Achievements)")
        st.markdown("""
            <div class="example-good">
            <b>Data Analyst | XYZ Corp | 2021-2023</b><br><br>
            • Analyzed 500K+ customer records using SQL and Python, identifying $2M in revenue opportunities<br>
            • Automated monthly reporting with Tableau dashboards, saving 20 hours/month<br>
            • Led cross-functional team of 4 to implement new analytics framework, improving data accuracy by 35%<br>
            • Presented insights to C-level executives, influencing strategic decisions worth $5M
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sample Job Descriptions Library
    st.markdown("#### 📚 Sample Job Descriptions Library")
    
    st.info("💡 Use these sample job descriptions to practice tailoring your resume")
    
    job_role_sample = st.selectbox(
        "Select a role to view sample job description:",
        ["Data Analyst", "Software Engineer", "Data Scientist", "Product Manager"]
    )
    
    job_descriptions = {
        "Data Analyst": """
**Data Analyst - Tech Company**

**Responsibilities:**
- Analyze large datasets to identify trends and insights
- Create dashboards and reports using Tableau and Power BI
- Work with SQL databases to extract and manipulate data
- Collaborate with business teams to understand requirements
- Present findings to stakeholders

**Required Skills:**
- 2+ years of experience in data analysis
- Strong SQL skills (MySQL, PostgreSQL)
- Proficiency in Excel (pivot tables, VLOOKUPs, macros)
- Experience with Python or R for statistical analysis
- Data visualization tools (Tableau, Power BI)
- Strong analytical and problem-solving skills
- Excellent communication skills

**Preferred:**
- Bachelor's degree in Statistics, Mathematics, or related field
- Experience with A/B testing
- Knowledge of statistical methods
        """,
        "Software Engineer": """
**Software Engineer - Startup**

**Responsibilities:**
- Design, develop, and maintain web applications
- Write clean, efficient, and well-documented code
- Participate in code reviews and testing
- Collaborate with product and design teams
- Deploy applications using CI/CD pipelines

**Required Skills:**
- 3+ years of software development experience
- Proficiency in Java, Python, or JavaScript
- Experience with React, Angular, or Vue.js
- Knowledge of RESTful APIs and microservices
- Understanding of databases (SQL and NoSQL)
- Git version control
- Agile/Scrum methodology

**Preferred:**
- Bachelor's degree in Computer Science
- AWS or Azure cloud experience
- Docker and Kubernetes knowledge
- Experience with testing frameworks
        """,
        "Data Scientist": """
**Data Scientist - Financial Services**

**Responsibilities:**
- Build and deploy machine learning models
- Conduct statistical analysis and hypothesis testing
- Clean and preprocess large datasets
- Develop predictive models for business problems
- Communicate findings to technical and non-technical audiences

**Required Skills:**
- Master's or PhD in Data Science, Statistics, or related field
- 3+ years of experience in data science or machine learning
- Expert in Python (scikit-learn, TensorFlow, PyTorch)
- Strong statistical and mathematical background
- Experience with SQL and big data technologies
- Data visualization skills

**Preferred:**
- Publications in ML/AI conferences
- Experience with NLP or computer vision
- Cloud platform experience (AWS SageMaker, Azure ML)
- Experience in financial industry
        """,
        "Product Manager": """
**Product Manager - SaaS Company**

**Responsibilities:**
- Define product vision and roadmap
- Gather and prioritize product requirements
- Work closely with engineering, design, and marketing teams
- Analyze product metrics and user feedback
- Lead product launches and go-to-market strategies

**Required Skills:**
- 5+ years of product management experience
- Strong understanding of agile methodologies
- Data-driven decision making
- Excellent communication and leadership skills
- Experience with product analytics tools
- Stakeholder management
- Technical background or ability to work with engineers

**Preferred:**
- MBA or technical degree
- Experience in SaaS products
- Knowledge of UX/UI principles
- SQL or data analysis skills
        """
    }
    
    st.markdown(f"""
        <div class="tip-card">
            <pre>{job_descriptions[job_role_sample]}</pre>
        </div>
    """, unsafe_allow_html=True)

# ---------------- ACTIONABLE CHECKLIST ----------------
st.markdown("---")
st.markdown("### ✅ Resume Optimization Checklist")

st.markdown("""
    <div class="tip-card">
        <h3>Before Submitting Your Resume</h3>
        <p>Use this checklist to ensure your resume is ATS-ready:</p>
    </div>
""", unsafe_allow_html=True)

checklist_items = [
    "Resume is saved as PDF or DOCX",
    "File name is professional (e.g., 'John_Doe_Resume.pdf')",
    "Contact information is at the top and complete",
    "No images, graphics, tables, or text boxes used",
    "Standard font (Arial, Calibri, Times New Roman) in 10-12pt",
    "Clear section headers (Experience, Education, Skills)",
    "Keywords from job description are naturally included",
    "All technical skills are listed in Skills section",
    "Each bullet point starts with a strong action verb",
    "Quantifiable achievements included (numbers, percentages)",
    "Resume is 1-2 pages maximum",
    "No spelling or grammatical errors",
    "Dates and formatting are consistent throughout",
    "Job titles and company names are clearly visible",
    "LinkedIn profile URL is included and updated"
]

col1, col2 = st.columns(2)

for i, item in enumerate(checklist_items):
    if i < len(checklist_items) // 2:
        with col1:
            st.checkbox(item, key=f"check_{i}")
    else:
        with col2:
            st.checkbox(item, key=f"check_{i}")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #008B8B;'>
        <p><i>💡 Remember: An ATS-friendly resume is also human-friendly!</i></p>
        <p><i>Keep it clear, concise, and focused on achievements.</i></p>
    </div>
""", unsafe_allow_html=True)
