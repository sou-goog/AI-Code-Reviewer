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
    Configure the Google Gemini API Key.
    """
    # For simplicity in this MVP, we will guide the user to set the env var.
    # In a full app, we might use a .env file or keyring.
    console.print(f"[bold yellow]To configure, please set the environment variable:[/bold yellow]")
    console.print(f"[code]setx GEMINI_API_KEY \"{api_key}\"[/code]")
    console.print("Then restart your terminal.")
    # We could also use dotenv, but let's keep it dependency-light for now or just tell them.

if __name__ == "__main__":
    app()
