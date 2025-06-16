import typer
from rich import print

app = typer.Typer(help="XOLO CLI – Tool for manage vfx and animation projects")

@app.command()
def init():
    """Initialize project  XOLO."""
    print("[bold green]✅ Xolo project initialized![/bold green]")

if __name__ == "__main__":
    app()
