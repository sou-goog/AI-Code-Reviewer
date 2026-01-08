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
    layout="wide"
)

# Title
st.title("🤖 AI Code Reviewer Dashboard")
st.markdown("*Powered by Google Gemini*")

# Sidebar
st.sidebar.header("⚙️ Settings")

# API Key check
api_key = os.environ.get("GEMINI_API_KEY", "")
if not api_key:
    st.sidebar.error("⚠️ GEMINI_API_KEY not set!")
    api_key_input = st.sidebar.text_input("Enter API Key:", type="password")
    if api_key_input:
        os.environ["GEMINI_API_KEY"] = api_key_input
else:
    st.sidebar.success("✅ API Key configured")

# Review options
diff_type = st.sidebar.selectbox(
    "Diff Type",
    ["staged", "uncommitted", "last-commit"],
    help="What changes to review"
)

# Load config
config = ConfigManager()

# Main content
tab1, tab2, tab3 = st.tabs(["📝 Review", "⚙️ Configuration", "📊 Stats"])

with tab1:
    st.header("Code Review")
    
    if st.button("🔍 Run Review", type="primary", use_container_width=True):
        with st.spinner("Analyzing code with AI..."):
            try:
                report = run_review(diff_type=diff_type, output_format="terminal")
                
                if "No" in report and "changes found" in report:
                    st.info(report)
                elif "Error" in report:
                    st.error(report)
                else:
                    st.markdown(report)
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Review",
                        data=report,
                        file_name=f"review-{diff_type}.md",
                        mime="text/markdown"
                    )
            except Exception as e:
                st.error(f"Error: {e}")

with tab2:
    st.header("Configuration")
    
    # Show current config
    st.subheader("Current Settings")
    st.json(config.config)
    
    st.info("💡 Edit `.codereview.yaml` to customize settings")
    
    # Custom Rules
    st.subheader("Custom Rules")
    custom_rules = config.get_custom_rules()
    
    if custom_rules:
        for i, rule in enumerate(custom_rules):
            with st.expander(f"Rule {i+1}: {rule.get('message', 'N/A')}"):
                st.code(f"Pattern: {rule.get('pattern', 'N/A')}")
                st.code(f"Severity: {rule.get('severity', 'N/A')}")
    else:
        st.warning("No custom rules configured")

with tab3:
    st.header("Review Statistics")
    
    st.info("📊 Review history and analytics coming soon!")
    
    # Placeholder stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Reviews Run", "-", help="Total reviews executed")
    
    with col2:
        st.metric("Issues Found", "-", help="Total issues detected")
    
    with col3:
        st.metric("Critical Issues", "-", help="High severity issues")

# Footer
st.markdown("---")
st.markdown("🔗 [GitHub Repository](https://github.com/sou-goog/AI-Code-Reviewer)")
