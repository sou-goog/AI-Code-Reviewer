import streamlit as st
import os
import sys
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
    }
    
    /* Hide default menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Title styling */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    /* Card styling */
    .stApp {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: transform 0.2s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea15 0%, #764ba215 100%);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        font-weight: 600;
    }
    
    /* Success/Error boxes */
    .stSuccess, .stError, .stInfo, .stWarning {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-title">🤖 AI Code Reviewer</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Powered by Google Gemini ✨</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # API Key check
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        st.error("⚠️ GEMINI_API_KEY not set!")
        api_key_input = st.text_input("Enter API Key:", type="password")
        if api_key_input:
            os.environ["GEMINI_API_KEY"] = api_key_input
            st.success("✅ Key configured!")
    else:
        st.success("✅ API Key configured")
    
    st.markdown("---")
    
    # Review options
    st.subheader("📋 Review Options")
    diff_type = st.selectbox(
        "Diff Type",
        ["staged", "uncommitted", "last-commit"],
        help="What changes to review"
    )
    
    st.markdown("---")
    
    # Quick links
    st.subheader("🔗 Quick Links")
    st.markdown("[📖 Documentation](https://github.com/sou-goog/AI-Code-Reviewer)")
    st.markdown("[🐛 Report Issue](https://github.com/sou-goog/AI-Code-Reviewer/issues)")
    st.markdown("[⭐ Star on GitHub](https://github.com/sou-goog/AI-Code-Reviewer)")

# Load config
config = ConfigManager()

# Main content
tab1, tab2, tab3 = st.tabs(["📝 Code Review", "⚙️ Configuration", "📊 Analytics"])

with tab1:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### Run AI Code Review")
        st.markdown("Analyze your code changes for bugs, security issues, and improvements.")
        
        if st.button("🚀 Analyze Code", type="primary", use_container_width=True):
            with st.spinner("🔍 AI is analyzing your code..."):
                try:
                    report = run_review(diff_type=diff_type, output_format="terminal")
                    
                    if "No" in report and "changes found" in report:
                        st.info(f"ℹ️ {report}")
                    elif "Error" in report:
                        st.error(f"❌ {report}")
                    else:
                        st.success("✅ Review Complete!")
                        st.markdown("---")
                        st.markdown(report)
                        
                        # Download section
                        st.markdown("---")
                        col_a, col_b, col_c = st.columns([1, 2, 1])
                        with col_b:
                            st.download_button(
                                label="📥 Download Review",
                                data=report,
                                file_name=f"review-{diff_type}.md",
                                mime="text/markdown",
                                use_container_width=True
                            )
                except Exception as e:
                    st.error(f"❌ Error: {e}")

with tab2:
    st.markdown("### Current Configuration")
    
    # Display config in nice format
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Review Settings")
        review_config = config.config.get('review', {})
        st.json(review_config)
    
    with col2:
        st.markdown("#### 🤖 Model Settings")
        model_config = config.config.get('model', {})
        st.json(model_config)
    
    st.markdown("---")
    
    # Custom Rules
    st.markdown("### 🎯 Custom Rules")
    custom_rules = config.get_custom_rules()
    
    if custom_rules:
        for i, rule in enumerate(custom_rules, 1):
            with st.expander(f"📌 Rule {i}: {rule.get('message', 'N/A')}", expanded=False):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.code(f"Pattern: {rule.get('pattern', 'N/A')}", language="text")
                with col_b:
                    severity = rule.get('severity', 'N/A')
                    st.code(f"Severity: {severity}", language="text")
    else:
        st.info("💡 No custom rules configured. Edit `.codereview.yaml` to add rules.")

with tab3:
    st.markdown("### 📊 Review Analytics")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Reviews",
            value="Coming Soon",
            delta=None,
            help="Total number of reviews run"
        )
    
    with col2:
        st.metric(
            label="Issues Found", 
            value="Coming Soon",
            delta=None,
            help="Total issues detected"
        )
    
    with col3:
        st.metric(
            label="Critical Issues",
            value="Coming Soon",
            delta=None,
            help="High severity issues"
        )
    
    with col4:
        st.metric(
            label="Files Reviewed",
            value="Coming Soon",
            delta=None,
            help="Total files analyzed"
        )
    
    st.markdown("---")
    st.info("📈 Advanced analytics with review history tracking coming in future updates!")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(
        '<p style="text-align: center; color: #6b7280;">Made with ❤️ using Streamlit & Google Gemini</p>',
        unsafe_allow_html=True
    )

