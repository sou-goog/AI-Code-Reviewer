# AI Code Reviewer - Local Setup Guide

## 🚀 Quick Start

### Backend (Terminal 1)
```powershell
cd api
python main.py
```
Server runs at: http://localhost:8000
API Docs: http://localhost:8000/docs

### Frontend (Terminal 2)
```powershell
cd frontend
npm install
npm run dev
```
App runs at: http://localhost:5173

## ✅ What's Running

**Backend API (Port 8000)**:
- FastAPI server wrapping your existing Python code
- CORS enabled for local development
- Endpoints: /api/review, /api/stats, /api/health

**Frontend (Port 5173)**:
- React + Vite + TailwindCSS
- Beautiful dark theme matching Replit design
- Real-time code review interface

## 🔑 Environment Setup

Make sure GEMINI_API_KEY is set:
```powershell
$env:GEMINI_API_KEY = "your_key_here"
```

## 📝 Test It

1. Open http://localhost:5173
2. Click "Load Sample" 
3. Click "Review Code"
4. See AI-powered results!

## 🛠️ Troubleshooting

**Port already in use?**
- Backend: Change port in api/main.py
- Frontend: Vite will auto-increment to :5174

**API not connecting?**
- Check backend is running on :8000
- Check GEMINI_API_KEY is set
- Check CORS in api/main.py

**Frontend not loading?**
- Run `npm install` in frontend/
- Check Node.js version (need 18+)
