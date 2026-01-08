# Troubleshooting Guide

## Common Issues and Solutions

### 1. API Key Issues

**Problem**: `GEMINI_API_KEY environment variable not set`

**Solution**:
```powershell
# Windows PowerShell
$env:GEMINI_API_KEY="your_key_here"

# Linux/Mac
export GEMINI_API_KEY="your_key_here"
```

**Verify**:
```bash
python -m src.main init
```

---

### 2. Git Repository Not Found

**Problem**: `Not a git repository`

**Solution**:
```bash
git init
# or make sure you're in a git repository directory
```

---

### 3. No Changes to Review

**Problem**: `No staged changes found to review`

**Solution**:
```bash
# Stage some files first
git add <files>

# Or review uncommitted changes
python -m src.main review --diff-type uncommitted
```

---

### 4. Import Errors

**Problem**: `ModuleNotFoundError: No module named 'src'`

**Solution**:
```bash
# Install dependencies
pip install -r requirements.txt

# Run from project root
cd "AI-Driven Automated Code Reviewer Agent"
python -m src.main review
```

---

### 5. Dashboard Won't Start

**Problem**: Streamlit errors or port conflicts

**Solution**:
```bash
# Kill existing streamlit processes
# Windows:
taskkill /F /IM streamlit.exe

# Linux/Mac:
pkill streamlit

# Start on different port
streamlit run dashboard.py --server.port 8502
```

---

### 6. Database Locked

**Problem**: `database is locked`

**Solution**:
```bash
# Close dashboard if running
# Wait a few seconds
# Try again

# If persistent, delete and recreate
rm reviews.db
# Database will be recreated automatically
```

---

### 7. GitHub Actions Not Running

**Problem**: Workflow doesn't trigger on PR

**Checklist**:
1. ✅ Workflow file in `.github/workflows/code-review.yml`
2. ✅ `GEMINI_API_KEY` secret added to repository settings
3. ✅ GitHub Actions enabled in repository settings
4. ✅ PR from non-main branch to main

**Debug**:
- Check Actions tab in GitHub for errors
- Verify secret is named exactly `GEMINI_API_KEY`
- Check workflow logs for API errors

---

### 8. Slow Reviews

**Problem**: Reviews take >10 seconds

**Causes**:
- Large diffs (>10 files)
- Gemini API congestion
- Network latency

**Solutions**:
- Review smaller changesets
- Split large PRs
- Wait and retry during off-peak hours

---

### 9. Inline Comments Not Posting

**Problem**: Comments appear as general, not inline

**Reason**: GitHub API limitations

**Explanation**:
- Inline comments require exact line matches
- If lines changed, falls back to general comment
- This is expected behavior

---

### 10. Test Failures

**Problem**: pytest failures on Windows

**Known Issue**: Database file locking on Windows

**Solution**:
```bash
# Tests work fine, just file cleanup issue
# Safe to ignore if tests pass functionally
pytest -v -k "not database"
```

---

## Installation Issues

### Windows

**PowerShell Execution Policy**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Long Path Issues**:
```powershell
# Enable long paths
git config --global core.longpaths true
```

### Linux/Mac

**Permission Errors**:
```bash
# Use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Performance Optimization

### Speed Up Reviews

1. **Reduce diff size**: Review smaller chunks
2. **Use caching**: Future feature (coming soon)
3. **Lighter model**: Try different Gemini models

### Reduce Memory Usage

1. Close dashboard when not needed
2. Limit database size (delete old reviews)
3. Use JSON output instead of terminal rendering

---

## Getting Help

1. **Check logs**: Look for error messages
2. **GitHub Issues**: https://github.com/sou-goog/AI-Code-Reviewer/issues
3. **Documentation**: Read README and ARCHITECTURE.md
4. **Debug mode**: Run with `--help` to see all options

---

## Debugging Tips

### Enable Verbose Output

```bash
# CLI shows more details
python -m src.main review --format json | jq .

# Check database contents
sqlite3 reviews.db "SELECT * FROM reviews ORDER BY timestamp DESC LIMIT 5;"
```

### Check API Connectivity

```python
# Test Gemini API
import os
import google.generativeai as genai

genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel('gemini-2.5-flash')
response = model.generate_content("Test")
print(response.text)
```

### Verify Git Integration

```bash
# Test git commands
git status
git diff --staged
git log -1 --oneline
```

---

## Reset Everything

If all else fails:

```bash
# Backup your config if you have one
cp .codereview.yaml .codereview.yaml.backup

# Clean install
rm -rf __pycache__ src/__pycache__ .pytest_cache
rm reviews.db
pip uninstall -y -r requirements.txt
pip install -r requirements.txt

# Reinitialize
python -m src.main init
```
