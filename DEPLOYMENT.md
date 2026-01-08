# 🚀 Quick Deployment Guide

## For Your Mentor Demo

### 1. Create GitHub Repo
```bash
# On GitHub, create new repo: "AI-Code-Reviewer"
# DON'T initialize with README (we already have one)
```

### 2. Push Code
```bash
git remote add origin https://github.com/YOUR_USERNAME/AI-Code-Reviewer.git
git branch -M main
git push -u origin main
```

### 3. Add Secret
1. Go to: `https://github.com/YOUR_USERNAME/AI-Code-Reviewer/settings/secrets/actions`
2. Click "New repository secret"
3. Name: `GEMINI_API_KEY`
4. Value: `AIzaSyDrdf_bTfsJ57DBsgSWzUXzcL-qfDTFPCk`
5. Save

### 4. Test It
```bash
# Create test branch
git checkout -b add-feature

# Make a change (add a file with a bug)
echo "def test(): return 1/0" > buggy.py
git add buggy.py
git commit -m "Add buggy function"

# Push and create PR
git push origin add-feature
```

Then go to GitHub and create a Pull Request. Wait 1-2 minutes for the AI review comment!

## What to Show Your Mentor

✅ **Working CLI tool** - Local code reviews  
✅ **Multiple output formats** - Terminal, Markdown, JSON  
✅ **Free deployment** - GitHub Actions (no server needed)  
✅ **Automatic PR reviews** - No manual intervention  
✅ **Production-ready docs** - README, setup guide

## Demo Script

1. Show the CLI: `python -m src.main review --help`
2. Show a local review: `python -m src.main review --format markdown`
3. Show the GitHub repo with the workflow
4. Show a Pull Request with AI comments
5. Discuss the roadmap (severity levels, custom rules, etc.)
