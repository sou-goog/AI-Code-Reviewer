# 🤖 AI Code Reviewer Agent

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?logo=github-actions)](https://github.com/features/actions)
[![Powered by Gemini](https://img.shields.io/badge/Powered%20by-Google%20Gemini-4285F4?logo=google)](https://ai.google.dev/)

> AI-powered code review tool using Google Gemini. Catch bugs, security issues, and style problems before you commit. **100% Free!**

## 🎬 Demo

Check out [PR #1](https://github.com/sou-goog/AI-Code-Reviewer/pull/1) to see the AI reviewer in action!

**What it catches:**
- 🔴 **Critical**: Security vulnerabilities, fatal bugs
- 🟡 **Warning**: Potential issues, code smells  
- 🟢 **Suggestion**: Best practices, optimizations
- ✅ **Positive**: Good practices worth highlighting

## ✨ Features

- 🔍 **Automated Code Analysis** - Reviews git diffs using AI
- 🆓 **100% Free** - Uses Google Gemini free tier
- 🎯 **Multiple Review Modes** - Staged, uncommitted, or last commit
- 📄 **Flexible Output** - Terminal, Markdown, or JSON
- ⚡ **Fast & Easy** - Simple CLI interface

## 🚀 Quick Start

### Installation

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

## 📖 Usage

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

## 🎣 Pre-commit Hooks (Optional)

Automatically review code before every commit:

```bash
# Install the hook
python setup_hooks.py

# Now reviews run automatically on git commit
# Press 'y' to proceed or 'n' to abort
```

To uninstall: `rm .git/hooks/pre-commit`

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
- **Google Gemini 2.5 Flash** (AI Model)
- **GitPython** (Git integration)
- **Typer** (CLI framework)
- **Rich** (Terminal UI)

## 🗺️ Roadmap

- [x] Basic CLI with staged changes review
- [x] Multiple diff types support
- [x] Output format options
- [x] Severity levels (🔴🟡🟢✅)
- [x] GitHub Actions integration
- [x] Pre-commit hooks
- [x] Configuration file support
- [ ] Custom review rules engine
- [ ] Multi-model support (Claude, GPT-4)
- [ ] Web dashboard
- [ ] Review history database
- [ ] Team analytics

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License

## 🤝 Contributing

Contributions welcome! Feel free to open issues or PRs.
