# 🤖 AI Code Reviewer Agent
# AI Code Reviewer

![Banner](banner.png)

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?logo=github-actions)](https://github.com/features/actions)
[![Powered by Gemini](https://img.shields.io/badge/Powered%20by-Google%20Gemini-4285F4?logo=google)](https://ai.google.dev/)

**Enterprise-grade AI-powered code review tool using Google Gemini.** Automatically analyzes code changes, provides intelligent feedback, and integrates seamlessly with your development workflow.Catch bugs, security issues, and style problems before you commit. **100% Free!**

## 🎬 Demo

Check out [PR #1](https://github.com/sou-goog/AI-Code-Reviewer/pull/1) to see the AI reviewer in action!

**What it catches:**
- 🔴 **Critical**: Security vulnerabilities, fatal bugs
- 🟡 **Warning**: Potential issues, code smells  
- 🟢 **Suggestion**: Best practices, optimizations
- ✅ **Positive**: Good practices worth highlighting

## ✨ What Makes This Special

- 🆓 **100% Free** - No costs for deployment or usage
- 🎯 **Production-Ready** - Full CI/CD with GitHub Actions
- 🔧 **Highly Configurable** - Custom rules, ignore patterns, model settings
- 🌐 **Multiple Interfaces** - CLI, Web Dashboard, GitHub Actions
- 📊 **Severity Categorization** - Critical, Warning, Suggestion levels
- 🎨 **Beautiful UI** - Modern, gradient-based web interface
- 🔒 **Extensible** - Easy to add new models and features

## 📚 Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - System design and diagrams
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and fixes
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [SECURITY.md](SECURITY.md) - Security policy
- [EXAMPLE_REVIEW.md](EXAMPLE_REVIEW.md) - Sample output

## ✨ Features

### 🔍 Intelligent Code Analysis
- **AI-Powered Reviews** - Leverages Google Gemini to analyze code changes
- **Multi-Level Severity** - Categorizes issues as 🔴 Critical, 🟡 Warning, 🟢 Suggestion, ✅ Positive
- **Security Focus** - Detects SQL injection, XSS, hardcoded secrets, and more
- **Performance Insights** - Identifies inefficient algorithms and memory issues

### ⚙️ Flexible Integration
- **CLI Tool** - Quick reviews from command line (`init`, `review`, `stats` commands)
- **Web Dashboard** - Beautiful Streamlit interface with real-time analytics
- **GitHub Actions** - Automatic PR reviews with **inline comments** on specific lines
- **Pre-commit Hooks** - Block commits with critical issues

### 🎯 Customization
- **Custom Rules** - Define your own pattern-based review criteria  
- **Multi-Language** - Python, JavaScript, Java, Go, Rust support
- **Configurable Models** - Switch between Gemini models
- **Ignore Patterns** - Exclude specific files or directories
- **Multiple Output Formats** - Terminal, Markdown, or JSON

### 📊 Analytics & Tracking
- **Review History** - SQLite database tracks all reviews
- **Real-time Dashboard** - Live metrics, pie charts, recent reviews
- **Performance Stats** - Duration tracking, issue counts by severity

## 🚀 Quick Start

### Option 1: Automated Setup
```bash
python quickstart.py
```
The script will:
- ✅ Check Python version
- ✅ Verify git installation  
- ✅ Install dependencies
- ✅ Validate your setup

### Option 2: Manual Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd AI-Driven\ Automated\ Code\ Reviewer\ Agent

# Install dependencies
pip install -r requirements.txt
```

### Setup API Key

1. Get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Set environment variable:
```powershell
# Windows
$env:GEMINI_API_KEY="your_api_key_here"

# Linux/Mac
export GEMINI_API_KEY="your_api_key_here"
```

### First Review

```bash
# Make some code changes
echo "def hello(): print('world')" > test.py

# Stage the changes  
git add test.py

# Run the review
python -m src.main review
```

See [EXAMPLE_REVIEW.md](EXAMPLE_REVIEW.md) for sample output.

## 📖 Usage

### Initialize in Your Project
```bash
python -m src.main init
```
This will:
- Verify git repository
- Check API  key setup
- Create `.codereview.yaml` config
- Show next steps

### Basic Review (Staged Changes)
```bash
python -m src.main review
```

### Review Uncommitted Changes
```bash
python -m src.main review --diff-type uncommitted
```

### Review Last Commit
```bash
python -m src.main review --diff-type last-commit
```

### Save as Markdown
```bash
python -m src.main review --format markdown
```

### Export as JSON
```bash
python -m src.main review --format json
```

### View Statistics
```bash
python -m src.main stats
```
Shows:
- Total reviews conducted
- Issues by severity
- Average review duration
- Recent review history

## 🎣 Pre-commit Hooks (Optional)

Automatically review code before every commit:

```bash
# Install the hook
python setup_hooks.py

# Now reviews run automatically on git commit
# Press 'y' to proceed or 'n' to abort
```

To uninstall: `rm .git/hooks/pre-commit`

## 🌐 Web Dashboard

Launch the interactive web interface:

```bash
streamlit run dashboard.py
```

Features:
- 📝 Interactive code reviews
- ⚙️ Configuration viewer
- 📊 Statistics (coming soon)
- 📥 Download reports

See [DASHBOARD.md](DASHBOARD.md) for deployment to Streamlit Cloud (free!).

## 🚀 GitHub Actions Deployment

### Automatic PR Reviews (Free!)

Set up automatic AI reviews on every Pull Request:

1. **Push to GitHub**:
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

2. **Add API Key Secret**:
   - Go to repo **Settings** → **Secrets and variables** → **Actions**
   - Add secret: `GEMINI_API_KEY` = your API key

3. **Create a PR** - The AI will automatically review and comment!

📖 See [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) for detailed instructions.

## �🛠️ Options

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `--diff-type` | `staged`, `uncommitted`, `last-commit` | `staged` | What changes to review |
| `--format` | `terminal`, `markdown`, `json` | `terminal` | Output format |

## ⚙️ Configuration

Create `.codereview.yaml` in your repo root to customize behavior:

```bash
cp .codereview.example.yaml .codereview.yaml
# Edit to your preferences
```

Example configuration:
- Ignore specific file patterns
- Set severity levels
- Add custom rules
- Configure AI model settings

## 📦 Tech Stack

- **Python 3.9+**
- **Google Generative AI** (Gemini 2.5 Flash - Free Tier)
- **GitPython** (Git integration)
- **Typer** (CLI framework)
- **Rich** (Terminal UI)

MIT License

## 🤝 Contributing

Contributions welcome! Feel free to open issues or PRs.
