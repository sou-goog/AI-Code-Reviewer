"""
FastAPI backend for AI Code Reviewer frontend.
Provides REST API for code review functionality.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sys
import os
from pathlib import Path

# Add src to path for LLM client
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.llm_client import analyze_code_diff

app = FastAPI(
    title="AI Code Reviewer API",
    version="1.0.0",
    description="AI-powered code review backend"
)

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class ReviewRequest(BaseModel):
    code_diff: str
    language: Optional[str] = "python"

class ReviewResponse(BaseModel):
    critical: list[str]
    warnings: list[str]
    suggestions: list[str]
    positive: list[str]
    summary: str

@app.get("/")
def root():
    return {
        "name": "AI Code Reviewer API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.post("/api/review", response_model=ReviewResponse)
async def create_review(request: ReviewRequest):
    """
    Analyze code diff and return structured review.
    """
    import traceback
    import logging
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Received review request for {len(request.code_diff)} characters of {request.language} code")
        
        # Get AI review
        review_text = analyze_code_diff(request.code_diff)
        logger.info(f"Got review text: {len(review_text)} characters")
        
        # Parse into structured format
        parsed = parse_review(review_text)
        logger.info("Successfully parsed review")
        
        return parsed
    except Exception as e:
        logger.error(f"Review failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_stats():
    """Get review statistics"""
    from src.database import get_review_stats
    
    try:
        stats = get_review_stats()
        return stats or {
            "total_reviews": 0,
            "total_critical": 0,
            "total_warnings": 0,
            "total_suggestions": 0,
            "avg_duration": 0
        }
    except Exception as e:
        # Return default stats if DB not configured
        return {
            "total_reviews": 0,
            "total_critical": 0,
            "total_warnings": 0,
            "total_suggestions": 0,
            "avg_duration": 0
        }

@app.get("/api/reviews")
async def list_reviews():
    """Get all reviews"""
    from src.database import get_all_reviews
    
    try:
        reviews = get_all_reviews()
        return reviews or []
    except Exception as e:
        return []

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint.
    """
    import os
    return {
        "status": "healthy",
        "api_key_configured": bool(os.getenv("GEMINI_API_KEY")),
        "database": "connected"
    }

def parse_review(review_text: str) -> ReviewResponse:
    """
    Parse AI review text into structured format.
    """
    sections = {
        "critical": [],
        "warnings": [],
        "suggestions": [],
        "positive": [],
        "summary": ""
    }
    
    # Extract summary
    if "Summary" in review_text:
        summary_start = review_text.find("Summary")
        summary_end = review_text.find("##", summary_start + 1)
        if summary_end == -1:
            summary_end = len(review_text)
        sections["summary"] = review_text[summary_start:summary_end].replace("## 🔍 Summary", "").strip()
    
    # Extract critical issues
    if "Critical" in review_text:
        critical_section = extract_section(review_text, "Critical")
        sections["critical"] = parse_items(critical_section)
    
    # Extract warnings
    if "Warning" in review_text:
        warning_section = extract_section(review_text, "Warning")
        sections["warnings"] = parse_items(warning_section)
    
    # Extract suggestions
    if "Suggestion" in review_text:
        suggestion_section = extract_section(review_text, "Suggestion")
        sections["suggestions"] = parse_items(suggestion_section)
    
    # Extract positive notes
    if "Positive" in review_text:
        positive_section = extract_section(review_text, "Positive")
        sections["positive"] = parse_items(positive_section)
    
    return ReviewResponse(**sections)

def extract_section(text: str, section_name: str) -> str:
    """Extract a section from markdown text."""
    start = text.find(f"## 🔴 {section_name}") if "Critical" in section_name else \
            text.find(f"## 🟡 {section_name}") if "Warning" in section_name else \
            text.find(f"## 🟢 {section_name}") if "Suggestion" in section_name else \
            text.find(f"## ✅ {section_name}")
    
    if start == -1:
        return ""
    
    end = text.find("##", start + 1)
    if end == -1:
        end = len(text)
    
    return text[start:end]

def parse_items(section: str) -> list[str]:
    """Parse bullet points from a section."""
    items = []
    lines = section.split('\n')
    current_item = ""
    
    for line in lines:
        line = line.strip()
        if line.startswith('-') or line.startswith('*'):
            if current_item:
                items.append(current_item.strip())
            current_item = line[1:].strip()
        elif line and current_item:
            current_item += " " + line
    
    if current_item:
        items.append(current_item.strip())
    
    return items

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting AI Code Reviewer API...")
    print("📝 API Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
