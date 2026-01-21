# 🚀 Deployment Guide

This guide will help you deploy the **AI Code Reviewer** application.

## ✅ Prerequisites

1.  **GitHub Account**: Ensure your code is pushed to a GitHub repository.

    > **IMPORTANT**: You currently have uncommitted changes on your local machine. You MUST commit and push them before deploying:
    >
    > ```bash
    > git add .
    > git commit -m "feat: add embedding and indexing services"
    > git push origin main
    > ```

2.  **API Keys**: You will need your `GEMINI_API_KEY` from [Google AI Studio](https://aistudio.google.com/).

---

## 🛠️ Backend Deployment (Render)

We will use **Render** to host the FastAPI backend for free.

1.  **Create Account**: Sign up at [render.com](https://render.com/).
2.  **New Web Service**:
    - Click **"New +"** and select **"Web Service"**.
    - Connect your GitHub repository.
3.  **Configure Service**:
    - **Name**: `ai-code-reviewer-api` (or similar)
    - **Region**: Closest to you (e.g., Oregon, Frankfurt)
    - **Branch**: `main`
    - **Runtime**: `Python 3`
    - **Build Command**: `pip install uvicorn fastapi && pip install -r api/requirements.txt`
    - **Start Command**: `cd api && python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
    - **Instance Type**: Free
4.  **Environment Variables**:
    - Scroll down to "Environment Variables".
    - Add Key: `GEMINI_API_KEY`
    - Add Value: `your_actual_api_key_here`
5.  **Deploy**: Click **"Create Web Service"**.
    - Wait for the build to finish.
    - **Copy the URL** of your deployed backend (e.g., `https://ai-code-reviewer-api.onrender.com`). You will need this for the frontend.

---

---

## 🎨 Frontend Deployment

You can choose either **Vercel** or **Netlify**. Both are supported.

### Option A: Vercel (Recommended)

1.  **Create Account**: Sign up at [vercel.com](https://vercel.com/).
2.  **Add New Project**:
    - Click **"Add New..."** -> **"Project"**.
    - Import your GitHub repository.
3.  **Configure Project**:
    - Vercel should auto-detect the Vite settings.
    - **Framework Preset**: Vite
    - **Root Directory**: `frontend` (Edit this if it's not automatically selected).
4.  **Environment Variables**:
    - Expand **"Environment Variables"**.
    - Key: `VITE_API_URL`
    - Value: Your Render Backend URL (e.g., `https://ai-code-reviewer-api.onrender.com`) - **No trailing slash**.
5.  **Deploy**: Click **"Deploy"**.

### Option B: Netlify

1.  **Create Account**: Sign up at [netlify.com](https://www.netlify.com/).
2.  **New Site**:
    - Click **"Add new site"** -> **"Import from Git"**.
    - Select **GitHub** and choose your repository.
3.  **Configure Build**:
    - **Base directory**: `frontend`
    - **Build command**: `npm run build`
    - **Publish directory**: `frontend/dist`
4.  **Environment Variables**:
    - Click **"Show advanced"** or go to **"Site configuration" > "Environment variables"**.
    - Key: `VITE_API_URL`
    - Value: Your Render Backend URL.
5.  **Deploy**: Click **"Deploy site"**.

---

## 🔄 Final Verification

1.  Open your Netlify URL.
2.  The app should load effectively.
3.  Try submitting a code review. If it works, your full stack app is live! 🚀
