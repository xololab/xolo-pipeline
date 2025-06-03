import typer
from .core import project, config
app = typer.Typer()

app.add_typer(project.app, name="project")
app.add_typer(config.app, name="config")



if __name__ == "__main__":
    app()