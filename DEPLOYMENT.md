# 🚀 Deployment Commands

## ⚠️ IMPORTANT: Do This First
1. Go to https://github.com/new
2. **Sign in** to your GitHub account
3. Create repository:
   - Name: `AI-Code-Reviewer`
   - Description: "AI-powered code review tool using Google Gemini"
   - Public repository
   - **DO NOT** check: Initialize with README, .gitignore, or license
4. Click "Create repository"

## Then Run These Commands

```powershell
# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/AI-Code-Reviewer.git

# Push code to GitHub
git branch -M main
git push -u origin main
```

## Add API Key Secret

1. Go to: `https://github.com/YOUR_USERNAME/AI-Code-Reviewer/settings/secrets/actions`
2. Click "New repository secret"
3. Name: `GEMINI_API_KEY`
4. Value: `YOUR_API_KEY_HERE` (Get your free key from https://aistudio.google.com/app/apikey)
5. Click "Add secret"

⚠️ **IMPORTANT**: Never commit your API key to the repository! Always use GitHub Secrets.

## Test the Deployment

```powershell
# Create test branch
git checkout -b test-ai-review

# Add a file with intentional bug
echo "def divide(a, b): return a / b" > test_bug.py
git add test_bug.py
git commit -m "Add test function"

# Push and create PR
git push origin test-ai-review
```

Then:
1. Go to your GitHub repo
2. Click "Pull requests" → "New pull request"
3. Select `test-ai-review` branch
4. Create PR
5. Wait 1-2 minutes
6. AI review will appear as a comment! 🎉

---

**You're done!** Show this to your mentor.
