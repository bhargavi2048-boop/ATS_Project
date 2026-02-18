# 📊 Professional ATS Resume Scoring System

The **Professional ATS Resume Scoring System** is an AI-powered **multipage web application** with a beautiful **teal blue theme** that evaluates resumes against job descriptions using advanced analysis techniques. It helps job seekers understand how well their resumes align with Applicant Tracking Systems (ATS) and provides actionable insights to improve resume quality.

---

## 🎨 Design Features

- **🎨 Beautiful Teal Blue Theme**: Consistent teal color scheme throughout all pages
- **📄 Multipage Architecture**: Organized into 5 dedicated pages for optimal user experience
- **💻 Responsive Design**: Clean, modern interface with gradient backgrounds and card-based layouts
- **📊 Interactive Visualizations**: Teal-themed charts and graphs for data presentation
- **✨ Smooth Navigation**: Easy-to-use sidebar navigation between different sections

---

## 📱 Application Pages

### 🏠 Home Page (`app.py`)
- Welcome section with feature highlights
- Quick stats and metrics dashboard
- System overview and how it works
- User testimonials
- Getting started guide

### 📊 Resume Scoring Page
- Upload single or multiple PDF resumes
- Select job role and paste job description
- Comprehensive ATS scoring across 6 categories:
  - Technical Skills
  - Experience Match
  - Soft Skills
  - Resume Quality
  - Searchability
  - Metrics Usage
- Visual score breakdown with teal-themed charts
- Keyword and skills detection
- Resume structure analysis
- Personalized improvement recommendations
- Resume strengths identification
- Multi-resume ranking and comparison
- Professional PDF report generation

### 📈 Analytics Dashboard
- Key Performance Indicators (KPIs)
- Score distribution charts
- Category performance analysis
- Popular job roles statistics
- Monthly usage trends
- Interactive filters and customization
- Benchmarking by role
- Export options (PNG, CSV, PDF)

### 💡 Tips & Guide Page
- General resume writing best practices
- Do's and Don'ts for ATS-friendly resumes
- Technical skills listing guidelines
- Formatting recommendations
- Keyword optimization strategies
- Before/after examples
- Sample job descriptions library
- Resume optimization checklist

### ℹ️ About Page
- System overview and mission
- Detailed analysis process explanation
- Scoring methodology breakdown
- Technology stack information
- System architecture diagram
- Frequently Asked Questions (FAQ)
- Developer information

---

## 🚀 Key Features

- **Multipage Navigation**: Organized content across 5 dedicated pages
- **Teal Blue Theme**: Beautiful, consistent color scheme throughout
- **Multiple Resume Analysis**: Upload and compare multiple resumes
- **Comprehensive Scoring**: 6-category evaluation system
- **Intelligent Analysis**: Keyword extraction, skills identification, structure analysis
- **Visual Analytics**: Interactive charts and graphs
- **Detailed Feedback**: Personalized recommendations and insights
- **Professional Reports**: Downloadable PDF reports with full analysis
- **Resume Ranking**: Compare and rank multiple resumes side-by-side
- **Tips Library**: Comprehensive guide for resume optimization
- **Sample Job Descriptions**: Pre-loaded examples for practice

---

## 🛠️ Technology Stack

- **Python 3.10+**
- **Streamlit** – Multipage web application framework
- **PyPDF2** – Resume PDF text extraction
- **Matplotlib** – Teal-themed data visualizations
- **ReportLab** – Professional PDF report generation
- **Regular Expressions** – Pattern matching and keyword detection
- **HTML/CSS** – Custom styling for teal blue theme

---

## ⚙️ Installation Guide

### Prerequisites
```bash
Python 3.10 or higher
```

### Install Dependencies
```bash
pip install streamlit PyPDF2 reportlab matplotlib numpy
```

### 📁 Project Structure
```
ATS_Project/
├── app.py                          # Home/Landing page
├── pages/
│   ├── 1_📊_Resume_Scoring.py     # Resume analysis page
│   ├── 2_📈_Analytics.py          # Analytics dashboard
│   ├── 3_💡_Tips_Guide.py         # Tips and best practices
│   └── 4_ℹ️_About.py              # About and FAQ
├── README.md                       # Documentation
└── Resume_Scoring_System.py        # Legacy single-page version
```

---

## ▶️ Run the Application

### Start the Multipage App
```bash
streamlit run app.py
```

### Access the Application
Open your browser and navigate to:
```
http://localhost:8501
```

### Navigate Through Pages
Use the sidebar to switch between:
- 🏠 Home
- 📊 Resume Scoring
- 📈 Analytics
- 💡 Tips Guide
- ℹ️ About

---

## 📊 How to Use

### 1. Upload Your Resume
- Navigate to the **Resume Scoring** page
- Select your target job role
- (Optional) Paste the job description for better matching
- Upload one or more PDF resumes

### 2. Get Analysis
- Click **"Analyze Resume(s)"**
- View comprehensive scores across 6 categories
- See detected skills and keywords
- Review resume structure analysis

### 3. Review Recommendations
- Read personalized improvement suggestions
- Identify resume strengths
- Compare multiple resumes if uploaded

### 4. Download Report
- Download professional PDF report with all findings
- Share with career counselors or keep for reference

### 5. Explore Other Features
- Check **Analytics** for industry benchmarks
- Read **Tips & Guide** for best practices
- Visit **About** for FAQ and system details

---

## 📄 Output Generated

- **Overall ATS Score**: Percentage match score
- **Category Breakdown**: Scores for each of 6 categories
- **Visual Charts**: Teal-themed bar charts and graphs
- **Skills Detected**: Technical and soft skills found
- **Structure Analysis**: Evaluation of resume sections
- **Improvement Tips**: Personalized recommendations
- **Resume Strengths**: Identified positive aspects
- **Professional PDF Report**: Comprehensive downloadable report
- **Multi-Resume Ranking**: Comparison table for multiple uploads

---

## ✅ Advantages

- **Multipage Design**: Better organization and user experience
- **Beautiful Theme**: Consistent teal blue color scheme
- **Comprehensive Analysis**: 6-category evaluation system
- **Multiple Resume Support**: Compare different versions
- **Actionable Insights**: Clear, specific recommendations
- **Professional Reports**: Polished PDF output
- **Educational Resources**: Built-in tips and guides
- **User-Friendly**: Intuitive interface with clear navigation
- **Free to Use**: No cost, no signup required

---

## 🎯 Use Cases

- **Job Seekers**: Optimize resumes before applying
- **Career Services**: Help students improve resumes
- **Resume Writers**: Validate resume quality
- **Recruiters**: Understand ATS behavior
- **Career Coaches**: Provide data-driven feedback
- **Students**: Learn resume best practices

---

## ⚠️ Limitations

- PDF format only (no Word documents)
- English-language resumes only
- ATS logic is simulated (not company-specific)
- Accuracy depends on resume text quality
- Image-based PDFs cannot be processed

---

## 🔮 Future Enhancements

- **User Accounts**: Save analysis history
- **More File Formats**: Support for .docx files
- **Real-time Editing**: In-app resume editor
- **AI-Powered Suggestions**: GPT-based recommendations
- **Company-Specific ATS**: Integration with actual ATS systems
- **Multilingual Support**: Analyze resumes in multiple languages
- **Mobile App**: iOS and Android applications
- **API Access**: Integration with other career tools

---

## 📚 Documentation

### For Developers
- All pages are in the `pages/` directory
- Naming convention: `{order}_{icon}_{name}.py`
- Shared teal color constants in each file
- Custom CSS for consistent theming
- Modular function design for reusability

### For Users
- Comprehensive FAQ in the About page
- Detailed tips in the Tips & Guide page
- Interactive examples and templates
- Sample job descriptions for practice

---

## 🤝 Contributing

This project is open for contributions! Areas for improvement:
- Enhanced NLP algorithms
- Additional job roles and industries
- More visualization options
- Mobile responsiveness improvements
- Accessibility features

---

## 📌 Conclusion

The **Professional ATS Resume Scoring System** is a comprehensive, multipage web application designed to help job seekers create ATS-friendly resumes. With its beautiful teal blue theme, intuitive navigation, and powerful analysis features, it provides everything needed to optimize resumes and improve chances of landing interviews.

---

## 👩‍💻 Author

**Bhargavi**  
Professional ATS Resume Scoring System  

💼 Making job applications more accessible and transparent for everyone.

---

## 📄 License

This project is created for educational and career development purposes.

---

## 🙏 Acknowledgments

- Streamlit community for the amazing framework
- Open source libraries that power this application
- Job seekers worldwide who inspired this tool

---

**⭐ If this tool helped you, please star the repository!**
