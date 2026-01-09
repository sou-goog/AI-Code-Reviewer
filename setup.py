"""
Package setup configuration for AI Code Reviewer.
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="ai-code-reviewer",
    version="1.0.0",
    author="Sougata",
    description="Enterprise-grade AI-powered code review tool using Google Gemini",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sou-goog/AI-Code-Reviewer",
    project_urls={
        "Bug Tracker": "https://github.com/sou-goog/AI-Code-Reviewer/issues",
        "Documentation": "https://github.com/sou-goog/AI-Code-Reviewer#readme",
        "Source Code": "https://github.com/sou-goog/AI-Code-Reviewer",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "typer[all]>=0.9.0",
        "rich>=13.0.0",
        "gitpython>=3.1.0",
        "google-generativeai>=0.3.0",
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.11.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
            "types-PyYAML>=6.0.0",
        ],
        "dashboard": [
            "streamlit>=1.28.0",
            "plotly>=5.17.0",
            "pandas>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "code-reviewer=main:app",
        ],
    },
    keywords="code-review ai gemini automation github ci-cd",
)
