import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Analytics | ATS System", page_icon="📈", layout="wide")

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
    
    .analytics-card {
        background: linear-gradient(135deg, #E0FFFF 0%, #AFEEEE 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #008B8B;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 139, 139, 0.2);
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #20B2AA;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 139, 139, 0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #008B8B;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #006666;
        margin-top: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
    <div class="main-header">
        <h1>📈 Analytics Dashboard</h1>
        <p>Comprehensive Resume Performance Insights & Trends</p>
    </div>
""", unsafe_allow_html=True)

# ---------------- GENERATE SAMPLE DATA ----------------
def generate_sample_analytics_data():
    """Generate sample analytics data for demonstration."""
    return {
        'total_resumes': 1247,
        'avg_score': 67.5,
        'pass_rate': 58.3,
        'improvement_rate': 23.4,
        'popular_roles': {
            'Data Analyst': 285,
            'Software Engineer': 312,
            'Data Scientist': 198,
            'Web Developer': 176,
            'Business Analyst': 145,
            'Product Manager': 89,
            'DevOps Engineer': 42
        },
        'score_distribution': {
            '0-20': 45,
            '21-40': 123,
            '41-60': 342,
            '61-80': 456,
            '81-100': 281
        },
        'category_averages': {
            'Technical Skills': 62.3,
            'Experience Match': 58.7,
            'Soft Skills': 71.2,
            'Resume Quality': 69.8,
            'Searchability': 75.4,
            'Metrics Usage': 54.6
        },
        'monthly_trend': {
            'Jan': 89,
            'Feb': 94,
            'Mar': 102,
            'Apr': 118,
            'May': 125,
            'Jun': 138
        }
    }

data = generate_sample_analytics_data()

# ---------------- KEY METRICS ----------------
st.markdown("### 📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{data['total_resumes']:,}</div>
            <div class="metric-label">Total Resumes Analyzed</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{data['avg_score']}%</div>
            <div class="metric-label">Average ATS Score</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{data['pass_rate']}%</div>
            <div class="metric-label">Pass Rate (>70%)</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">+{data['improvement_rate']}%</div>
            <div class="metric-label">Avg Score Improvement</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---------------- CHARTS SECTION ----------------
st.markdown("### 📊 Visual Analytics")

# Row 1: Score Distribution and Category Performance
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🎯 Score Distribution")
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    ranges = list(data['score_distribution'].keys())
    counts = list(data['score_distribution'].values())
    colors_bars = [TEAL_LIGHT, TEAL_SECONDARY, '#FFD700', TEAL_PRIMARY, TEAL_DARK]
    
    bars = ax.bar(ranges, counts, color=colors_bars, edgecolor='white', linewidth=1.5)
    ax.set_xlabel('Score Range (%)', fontweight='bold', color=TEAL_DARK)
    ax.set_ylabel('Number of Resumes', fontweight='bold', color=TEAL_DARK)
    ax.set_title('Resume Score Distribution', fontsize=14, fontweight='bold', color=TEAL_DARK)
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold', color=TEAL_DARK)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    st.info("📊 Most resumes score between 61-80%, showing good ATS compatibility")

with col2:
    st.markdown("#### 📈 Category Performance")
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    categories = list(data['category_averages'].keys())
    scores = list(data['category_averages'].values())
    
    # Wrap long labels
    categories_wrapped = [cat.replace(' ', '\n') if len(cat) > 12 else cat for cat in categories]
    
    colors_bars = [TEAL_PRIMARY if s >= 70 else TEAL_SECONDARY for s in scores]
    bars = ax.bar(range(len(categories_wrapped)), scores, color=colors_bars, 
                   edgecolor='white', linewidth=1.5)
    
    ax.set_xticks(range(len(categories_wrapped)))
    ax.set_xticklabels(categories_wrapped, rotation=0, ha='center', fontsize=9)
    ax.set_ylabel('Average Score (%)', fontweight='bold', color=TEAL_DARK)
    ax.set_title('Average Scores by Category', fontsize=14, fontweight='bold', color=TEAL_DARK)
    ax.set_ylim(0, 100)
    ax.axhline(y=70, color='red', linestyle='--', linewidth=1, alpha=0.5)
    ax.text(0.5, 72, 'Target: 70%', color='red', fontsize=9)
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar, score in zip(bars, scores):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{score:.1f}%',
                ha='center', va='bottom', fontsize=9, fontweight='bold', color=TEAL_DARK)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    st.info("📊 Searchability performs best, while Metrics Usage needs improvement")

st.markdown("---")

# Row 2: Popular Roles and Monthly Trend
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 💼 Most Popular Job Roles")
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    roles = list(data['popular_roles'].keys())
    counts = list(data['popular_roles'].values())
    
    # Create horizontal bar chart
    y_pos = np.arange(len(roles))
    bars = ax.barh(y_pos, counts, color=TEAL_PRIMARY, edgecolor='white', linewidth=1.5)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(roles)
    ax.invert_yaxis()
    ax.set_xlabel('Number of Resumes', fontweight='bold', color=TEAL_DARK)
    ax.set_title('Top Job Roles', fontsize=14, fontweight='bold', color=TEAL_DARK)
    ax.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for i, (bar, count) in enumerate(zip(bars, counts)):
        ax.text(count + 5, i, str(count), va='center', fontweight='bold', color=TEAL_DARK)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    st.info("💼 Software Engineer and Data Analyst are the most analyzed roles")

with col2:
    st.markdown("#### 📅 Monthly Analysis Trend")
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    months = list(data['monthly_trend'].keys())
    values = list(data['monthly_trend'].values())
    
    ax.plot(months, values, marker='o', linewidth=3, markersize=10, 
            color=TEAL_PRIMARY, markerfacecolor=TEAL_SECONDARY, 
            markeredgecolor='white', markeredgewidth=2)
    ax.fill_between(range(len(months)), values, alpha=0.3, color=TEAL_LIGHT)
    
    ax.set_xlabel('Month (2024)', fontweight='bold', color=TEAL_DARK)
    ax.set_ylabel('Resumes Analyzed', fontweight='bold', color=TEAL_DARK)
    ax.set_title('Monthly Usage Trend', fontsize=14, fontweight='bold', color=TEAL_DARK)
    ax.grid(True, alpha=0.3)
    
    # Add value labels
    for i, (month, value) in enumerate(zip(months, values)):
        ax.text(i, value + 3, str(value), ha='center', fontweight='bold', color=TEAL_DARK)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    st.info("📈 Steady growth with 55% increase from January to June")

st.markdown("---")

# ---------------- INSIGHTS SECTION ----------------
st.markdown("### 💡 Key Insights & Recommendations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="analytics-card">
            <h4>📊 Top Performing Areas</h4>
            <ul>
                <li><b>Searchability (75.4%):</b> Most resumes use good keywords</li>
                <li><b>Soft Skills (71.2%):</b> Strong emphasis on interpersonal abilities</li>
                <li><b>Resume Quality (69.8%):</b> Generally well-structured resumes</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="analytics-card">
            <h4>🎯 Success Factors</h4>
            <ul>
                <li>Resumes with 5+ technical skills score 28% higher</li>
                <li>Including metrics increases scores by average 15%</li>
                <li>ATS-friendly formatting improves pass rate by 34%</li>
                <li>Tailored job descriptions improve matching by 22%</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="analytics-card">
            <h4>⚠️ Areas Needing Improvement</h4>
            <ul>
                <li><b>Metrics Usage (54.6%):</b> Many resumes lack quantifiable achievements</li>
                <li><b>Experience Match (58.7%):</b> Better keyword alignment needed</li>
                <li><b>Technical Skills (62.3%):</b> Need more relevant tech skills</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="analytics-card">
            <h4>💼 Industry Trends</h4>
            <ul>
                <li>Tech roles dominate with 67% of all submissions</li>
                <li>Average time to improve resume: 2-3 iterations</li>
                <li>Most common missing skill: SQL/Database management</li>
                <li>Best improvement area: Adding quantifiable metrics</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---------------- COMPARISON TABLE ----------------
st.markdown("### 📋 Score Benchmarks by Role")

benchmark_data = {
    "Job Role": ["Data Analyst", "Data Scientist", "Software Engineer", "Web Developer", "Business Analyst"],
    "Avg Score": ["68.5%", "71.2%", "69.8%", "65.4%", "67.1%"],
    "Top Skill Required": ["SQL, Excel", "Python, ML", "Java, Git", "HTML, CSS", "Analytics, Excel"],
    "Pass Rate": ["62%", "67%", "64%", "58%", "61%"],
    "Difficulty": ["Medium", "Hard", "Hard", "Medium", "Medium"]
}

st.dataframe(benchmark_data, use_container_width=True)

st.info("💡 **Tip:** Compare your score against role-specific benchmarks to understand your competitiveness")

# ---------------- INTERACTIVE FILTERS ----------------
st.markdown("---")
st.markdown("### 🔍 Custom Analytics (Interactive)")

col1, col2, col3 = st.columns(3)

with col1:
    selected_role = st.selectbox(
        "Filter by Role",
        ["All Roles", "Data Analyst", "Software Engineer", "Data Scientist"]
    )

with col2:
    selected_period = st.selectbox(
        "Time Period",
        ["Last 30 Days", "Last 90 Days", "Last 6 Months", "All Time"]
    )

with col3:
    score_filter = st.slider(
        "Minimum Score",
        0, 100, 0
    )

if st.button("🔄 Apply Filters", use_container_width=True):
    st.success(f"✅ Showing analytics for {selected_role} in {selected_period} with scores ≥ {score_filter}%")
    st.info("📊 In the full version, this would show filtered real-time data")

# ---------------- EXPORT OPTIONS ----------------
st.markdown("---")
st.markdown("### 📥 Export Options")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Export Charts (PNG)", use_container_width=True):
        st.info("Charts will be exported as PNG images")

with col2:
    if st.button("📈 Export Data (CSV)", use_container_width=True):
        st.info("Analytics data will be exported as CSV")

with col3:
    if st.button("📄 Generate Report (PDF)", use_container_width=True):
        st.info("Comprehensive analytics report will be generated")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #008B8B;'>
        <p><i>📈 Analytics data updates in real-time as resumes are analyzed</i></p>
        <p><i>Last updated: {}</i></p>
    </div>
""".format(datetime.now().strftime('%B %d, %Y at %I:%M %p')), unsafe_allow_html=True)
