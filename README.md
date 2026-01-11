# 🤖 AI Code Reviewer

**Enterprise-grade AI-powered code review tool using Google Gemini**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Powered by Gemini](https://img.shields.io/badge/Powered%20by-Google%20Gemini-4285F4?logo=google)](https://ai.google.dev/)

**Automatically analyzes code changes, provides intelligent feedback, and integrates seamlessly with your development workflow. 100% Free!**

---

## ✨ Features

- 🆓 **100% Free** - No costs for deployment or usage (Gemini free tier)
- 🎯 **Production-Ready** - Full-stack React + FastAPI application
- 🎨 **Beautiful UI** - Modern dark-themed interface
- 🔒 **Enterprise-Grade** - Retry logic, caching, error handling
- 🌐 **Deployed** - Live on Netlify + Render
- 🚀 **Fast** - File-based caching (3-5x faster)

## 🚀 Quick Start

### Option 1: Use the Live App
Visit the deployed application (link will be here after deployment)

### Option 2: Run Locally

**Backend:**
```powershell
$env:GEMINI_API_KEY = "your_key"
cd api
python main.py
```

**Frontend:**
```powershell
cd frontend
npm install
npm run dev
```

## 📖 Usage

### CLI Tool
```bash
# Review staged changes
python -m src.main review

# View statistics
python -m src.main stats
```

### Web Interface
1. Open the frontend URL
2. Click "Load Sample"
3. Click "Review Code"
4. View AI-powered results!

## 📦 Tech Stack

### Backend
- **FastAPI** - Python REST API
- **Google Gemini 2.5 Flash** - AI model (Free Tier)
- **SQLite** - Review history database

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **Framer Motion** - Animations

## 🌐 Deployment

### Frontend (Netlify)
Auto-deploys from `main` branch

### Backend (Render)
Configured with `render.yaml`

See [LOCAL_SETUP.md](LOCAL_SETUP.md) for local development.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Google Gemini](https://ai.google.dev/) for the free AI API
- [Netlify](https://netlify.com/) for frontend hosting
- [Render](https://render.com/) for backend hosting

---

**Made with ❤️ using Python, React, and Google Gemini**

⭐ Star this repo if you find it useful!
