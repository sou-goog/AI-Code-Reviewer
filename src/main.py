import typer
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command()
def review(
    diff_type: str = typer.Option("staged", help="Type of changes: staged, uncommitted, last-commit"),
    format: str = typer.Option("terminal", help="Output format: terminal, markdown, json")
):
    """
    Analyze changes in the current git repository.
    """
    console.print("[bold green]🔍 Starting Code Review...[/bold green]")
    
    try:
        from src.reviewer import run_review
        
        with console.status("[bold blue]Analyzing code with AI...[/bold blue]"):
            report = run_review(diff_type=diff_type, output_format=format)
        
        if format == "terminal":
            from rich.markdown import Markdown
            md = Markdown(report)
            console.print(md)
        elif format == "markdown":
            filename = f"review-{diff_type}.md"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(report)
            console.print(f"[green]✓ Review saved to {filename}[/green]")
        elif format == "json":
            import json
            output = {"diff_type": diff_type, "review": report}
            print(json.dumps(output, indent=2))
    except KeyboardInterrupt:
        console.print("\n[yellow]Review cancelled.[/yellow]")
    except Exception as e:
        console.print(f"[bold red]❌ An error occurred:[/bold red] {e}")
        console.print("[dim]Tip: Make sure GEMINI_API_KEY is set and you're in a git repository.[/dim]")

@app.command()
def config(api_key: str):
    """
    Guide for configuring the GEMINI_API_KEY.
    """
    console.print("[bold yellow]🔑 API Key Configuration[/bold yellow]\n")
    console.print("Set your GEMINI_API_KEY environment variable:")
    console.print("\n[bold]Windows (PowerShell):[/bold]")
    console.print(f'  $env:GEMINI_API_KEY="{api_key}"')
    console.print("\n[bold]Linux/Mac:[/bold]")
    console.print(f'  export GEMINI_API_KEY="{api_key}"')
    console.print("\n[dim]Get a free API key: https://aistudio.google.com/app/apikey[/dim]")

@app.command()
def init():
    """
    Initialize AI Code Reviewer in current repository.
    """
    import os
    
    console.print("[bold green]🚀 Initializing AI Code Reviewer...[/bold green]\n")
    
    # Check if it's a git repo
    if not os.path.exists('.git'):
        console.print("[red]❌ Not a git repository. Run 'git init' first.[/red]")
        return
    
    console.print("✅ Git repository detected")
    
    # Check for API key
    if os.environ.get("GEMINI_API_KEY"):
        console.print("✅ GEMINI_API_KEY is set")
    else:
        console.print("[yellow]⚠️  GEMINI_API_KEY not set[/yellow]")
        console.print("   Get yours at: https://aistudio.google.com/app/apikey")
    
    # Create config file
    config_file = ".codereview.yaml"
    if not os.path.exists(config_file):
        import shutil
        if os.path.exists(".codereview.example.yaml"):
            shutil.copy(".codereview.example.yaml", config_file)
            console.print(f"✅ Created {config_file}")
        else:
            console.print(f"[yellow]⚠️  {config_file} template not found[/yellow]")
    else:
        console.print(f"✅ {config_file} already exists")
    
    console.print("\n[bold green]🎉 Setup complete![/bold green]")
    console.print("\nNext steps:")
    console.print("  1. Make some code changes")
    console.print("  2. Stage them: [bold]git add <files>[/bold]")
    console.print("  3. Run review: [bold]python -m src.main review[/bold]")

@app.command()
def stats():
    """
    Show review statistics from database.
    """
    from src.database import ReviewDatabase
    
    console.print("[bold blue]📊 Review Statistics[/bold blue]\n")
    
    try:
        db = ReviewDatabase()
        stats = db.get_review_stats()
        recent = db.get_recent_reviews(5)
        
        # Summary metrics
        console.print(f"[green]Total Reviews:[/green] {stats['total_reviews']}")
        console.print(f"[green]Average Duration:[/green] {stats['avg_duration']}s")
        
        issues = stats['total_issues']
        console.print(f"\n[red]🔴 Critical:[/red] {issues['critical']}")
        console.print(f"[yellow]🟡 Warning:[/yellow] {issues['warning']}")
        console.print(f"[blue]🟢 Suggestion:[/blue] {issues['suggestion']}")
        
        # Recent reviews
        if recent:
            console.print("\n[bold]Recent Reviews:[/bold]")
            for r in recent[:5]:
                total_issues = r['critical_count'] + r['warning_count'] + r['suggestion_count']
                console.print(f"  • {r['timestamp']} - {r['diff_type']} - {total_issues} issues ({r['duration_seconds']:.1f}s)")
        
    except Exception as e:
        console.print(f"[red]Error loading stats: {e}[/red]")


@app.command()
def version():
    """
    Show version information.
    """
    console.print("[bold cyan]AI Code Reviewer[/bold cyan]")
    console.print("Version: [green]1.0.0[/green]")
    console.print("Powered by [yellow]Google Gemini ✨[/yellow]")
    console.print("\nRepository: https://github.com/sou-goog/AI-Code-Reviewer")


@app.command()
def doctor():
    """
    Check if everything is configured correctly.
    """
    import sys
    import os
    from pathlib import Path
    
    console.print("[bold blue]🔍 System Health Check[/bold blue]\n")
    
    # Check Python version
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    py_ok = sys.version_info >= (3, 9)
    console.print(f"{'✅' if py_ok else '❌'} Python version: {py_version} {'(OK)' if py_ok else '(Need 3.9+)'}")
    
    # Check Git
    try:
        import git
        git_ok = True
        console.print("✅ Git: Installed")
    except Exception:
        git_ok = False
        console.print("❌ Git: Not found")
    
    # Check API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        console.print("✅ GEMINI_API_KEY: Configured")
    else:
        console.print("❌ GEMINI_API_KEY: Not set")
        console.print("   Get one at: https://aistudio.google.com/app/apikey")
    
    # Check database
    try:
        from src.database import ReviewDatabase
        db = ReviewDatabase()
        console.print(f"✅ Database: Accessible ({db.get_total_reviews()} reviews)")
    except Exception as e:
        console.print(f"❌ Database: Error ({e})")
    
    # Check cache directory
    cache_dir = Path.home() / ".code-reviewer" / "cache"
    if cache_dir.exists():
        from src.utils.cache import ReviewCache
        cache = ReviewCache()
        stats = cache.get_stats()
        console.print(f"✅ Cache: OK ({stats['count']} entries, {stats['total_size_mb']} MB)")
    else:
        console.print("⚠️  Cache: Not initialized (will be created on first review)")
    
    console.print("\n[bold green]Overall Status:[/bold green]")
    if py_ok and git_ok and api_key:
        console.print("✅ Ready to review code!")
    else:
        console.print("⚠️  Some components need attention (see above)")


if __name__ == "__main__":
    app()
