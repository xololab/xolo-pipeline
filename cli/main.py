import typer
from .commands import settings, show

app = typer.Typer(help="XOLO CLI – Tool for manage vfx and animation projects")





app.add_typer(settings.app, name="settings")
app.add_typer(show.app, name="show")

if __name__ == "__main__":
    app()
