# 🤖 AI Code Reviewer Agent

AI-powered code review tool using Google Gemini. Catch bugs, security issues, and style problems before you commit.

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

## � GitHub Actions Deployment

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
- [x] GitHub Actions integration
- [ ] Custom review rules
- [ ] Pre-commit hooks
- [ ] Severity levels
- [ ] Web dashboard

## 📄 License

MIT License

## 🤝 Contributing

Contributions welcome! Feel free to open issues or PRs.
