import streamlit as st
import os
import sys
import json
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.reviewer import run_review
from src.config import ConfigManager

st.set_page_config(
    page_title="AI Code Reviewer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #ec4899;
        --bg-color: #f8fafc;
        --card-bg: #ffffff;
    }
    
    /* Global Styles */
    .stApp {
        background-color: var(--bg-color);
        font-family: 'Inter', sans-serif;
    }
    
    /* Header & Title */
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1 0%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
        margin-bottom: 0.5rem;
        letter-spacing: -0.05em;
    }
    
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.25rem;
        margin-bottom: 3rem;
        font-weight: 500;
    }
    
    /* Custom Card Styling */
    .review-card {
        background-color: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid #e2e8f0;
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .review-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }

    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }

    .issue-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1e293b;
    }

    .file-badge {
        background-color: #f1f5f9;
        color: #475569;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 500;
        font-family: 'Monaco', 'Consolas', monospace;
    }

    /* Severity Badges */
    .badge {
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .badge-critical { background-color: #fee2e2; color: #ef4444; }
    .badge-warning { background-color: #fef9c3; color: #eab308; }
    .badge-suggestion { background-color: #dcfce7; color: #22c55e; }
    .badge-positive { background-color: #dbeafe; color: #3b82f6; }

    /* Description Text */
    .issue-desc {
        color: #334155;
        line-height: 1.6;
        font-size: 1rem;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        transition: all 0.2s;
    }
    
    .stButton>button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 1px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        border: none;
        background-color: transparent;
        color: #64748b;
        font-weight: 600;
        padding: 0;
    }

    .stTabs [aria-selected="true"] {
        color: #6366f1 !important;
        border-bottom: 2px solid #6366f1 !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }

    /* Metric Cards */
    div[data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def get_severity_color(severity):
    colors = {
        'critical': '#ef4444',
        'warning': '#eab308',
        'suggestion': '#22c55e',
        'positive': '#3b82f6'
    }
    return colors.get(severity.lower(), '#94a3b8')

def render_issue_card(issue):
    severity = issue.get('severity', 'info').lower()

    st.markdown(f"""
    <div class="review-card">
        <div class="card-header">
            <span class="badge badge-{severity}">{severity}</span>
            <span class="file-badge">📄 {issue.get('file', 'General')} : {issue.get('line', 'N/A')}</span>
        </div>
        <div class="issue-title">{issue.get('title', 'Issue Found')}</div>
        <div class="issue-desc">{issue.get('description', 'No description provided.')}</div>
    </div>
    """, unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-title">🤖 AI Code Reviewer</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Intelligent Code Analysis Powered by Gemini Pro</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    # API Key check
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        st.error("⚠️ GEMINI_API_KEY missing")
        api_key_input = st.text_input("Enter API Key:", type="password")
        if api_key_input:
            os.environ["GEMINI_API_KEY"] = api_key_input
            st.success("✅ Key configured!")
            st.rerun()
    else:
        st.success("✅ API Key Active")
    
    st.markdown("---")
    
    # Review options
    st.markdown("### 📋 Review Scope")
    diff_type = st.selectbox(
        "Select Changes",
        ["staged", "uncommitted", "last-commit"],
        format_func=lambda x: x.replace("-", " ").title(),
        help="Choose which changes to analyze"
    )
    
    st.markdown("---")
    
    # Quick links
    st.markdown("### 🔗 Resources")
    st.markdown("""
    <div style="display: flex; flex-direction: column; gap: 0.5rem;">
        <a href="https://github.com/sou-goog/AI-Code-Reviewer" style="text-decoration: none; color: #64748b;">📖 Documentation</a>
        <a href="https://github.com/sou-goog/AI-Code-Reviewer/issues" style="text-decoration: none; color: #64748b;">🐛 Report Bug</a>
    </div>
    """, unsafe_allow_html=True)

# Load config
config = ConfigManager()

# Main content
tab1, tab2, tab3 = st.tabs(["📝 Code Review", "⚙️ Configuration", "📊 Analytics"])

with tab1:
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        if st.button("🚀 Analyze Code Changes", type="primary", use_container_width=True):
            with st.spinner("🧠 AI is reading your code..."):
                try:
                    # Request JSON output
                    result = run_review(diff_type=diff_type, output_format="json")
                    
                    if isinstance(result, str):
                        # Fallback for text messages (errors or "no changes")
                        if "No" in result and "changes found" in result:
                            st.info(f"ℹ️ {result}")
                        else:
                            st.error(f"❌ {result}")
                    else:
                        # Process JSON result
                        issues = result.get('issues', [])
                        summary = result.get('summary', 'Review complete')
                        
                        st.success("✅ Analysis Complete!")
                        st.markdown(f"### 📋 Summary\n{summary}")

                        if issues:
                            st.markdown("---")

                            # Filters
                            severities = list(set(i.get('severity', 'info') for i in issues))
                            selected_severity = st.multiselect(
                                "Filter by Severity",
                                options=severities,
                                default=severities
                            )

                            filtered_issues = [i for i in issues if i.get('severity') in selected_severity]

                            if filtered_issues:
                                for issue in filtered_issues:
                                    render_issue_card(issue)
                            else:
                                st.info("No issues match selected filters.")

                        # Download JSON
                        st.markdown("---")
                        st.download_button(
                            label="📥 Download JSON Report",
                            data=json.dumps(result, indent=2),
                            file_name=f"review-{diff_type}.json",
                            mime="application/json",
                        )

                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")

with tab2:
    st.markdown("### 🛠️ Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown("#### 🎯 Review Rules")
            review_config = config.config.get('review', {})
            st.json(review_config)

    with col2:
        with st.container():
            st.markdown("#### 🤖 Model Parameters")
            model_config = config.config.get('model', {})
            st.json(model_config)
    
    st.markdown("---")
    st.markdown("#### 🔧 Custom Pattern Matching")
    
    custom_rules = config.get_custom_rules()
    if custom_rules:
        for i, rule in enumerate(custom_rules, 1):
            with st.expander(f"Rule {i}: {rule.get('message', 'Custom Rule')}"):
                st.markdown(f"**Pattern:** `{rule.get('pattern')}`")
                st.markdown(f"**Severity:** `{rule.get('severity')}`")
    else:
        st.info("💡 No custom rules defined. Add them to `.codereview.yaml`")

with tab3:
    st.markdown("### 📊 Performance Analytics")
    
    try:
        from src.database import ReviewDatabase
        db = ReviewDatabase()
        stats = db.get_review_stats()
        recent_reviews = db.get_recent_reviews(10)
        
        # Top Metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Reviews", stats['total_reviews'])
        m2.metric("Total Issues", sum(stats['total_issues'].values()))
        m3.metric("Avg Duration", f"{stats['avg_duration']}s")
        m4.metric("Critical Bugs", stats['total_issues']['critical'])
        
        st.markdown("---")
        
        # Charts
        c1, c2 = st.columns(2)

        with c1:
            st.subheader("Severity Distribution")
            if sum(stats['total_issues'].values()) > 0:
                fig = px.pie(
                    names=['Critical', 'Warning', 'Suggestion'],
                    values=[
                        stats['total_issues']['critical'],
                        stats['total_issues']['warning'],
                        stats['total_issues']['suggestion']
                    ],
                    color_discrete_sequence=['#ef4444', '#eab308', '#22c55e'],
                    hole=0.4
                )
                fig.update_layout(showlegend=True, height=350, margin=dict(t=0,b=0,l=0,r=0))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available yet")

        with c2:
            st.subheader("Recent Activity")
            if recent_reviews:
                # Prepare data for line chart
                import pandas as pd
                df = pd.DataFrame(recent_reviews)
                df['total_issues'] = df['critical_count'] + df['warning_count'] + df['suggestion_count']

                fig = px.bar(
                    df,
                    x='timestamp',
                    y='total_issues',
                    color='diff_type',
                    title='Issues per Review',
                    labels={'total_issues': 'Issues Found', 'timestamp': 'Date'}
                )
                fig.update_layout(height=350, margin=dict(t=30,b=0,l=0,r=0))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Run your first review to see trends")

    except Exception as e:
        st.error(f"Failed to load analytics: {e}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #94a3b8; padding: 2rem;">
        <p>Built with Streamlit & Google Gemini</p>
    </div>
    """,
    unsafe_allow_html=True
)
