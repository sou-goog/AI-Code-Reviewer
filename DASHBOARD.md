# AI Code Reviewer - Web Dashboard

## 🚀 Quick Start

```bash
streamlit run dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`

## ✨ Features

- **Interactive Review** - Run code reviews through web UI
- **Configuration Viewer** - See current settings from `.codereview.yaml`
- **Custom Rules Display** - View all active custom rules
- **Download Reports** - Save reviews as markdown files

## 📸 Screenshots

![Dashboard](dashboard-screenshot.png)

## 🌐 Cloud Deployment (Free!)

Deploy to Streamlit Cloud:

1. Push to GitHub (already done)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo
4. Add `GEMINI_API_KEY` to secrets
5. Click "Deploy"

**Your dashboard will be live at**: `https://your-app.streamlit.app`

## 📋 Requirements

- Python 3.9+
- All dependencies in `requirements.txt`
- `GEMINI_API_KEY` environment variable

## 🎯 Usage

1. Set API key in sidebar (or use environment variable)
2. Select diff type (staged, uncommitted, last-commit)
3. Click "Run Review"
4. View results and download if needed
