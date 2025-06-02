import typer
from rich.console import Console
from rich.table import Table
from pathlib import Path
import json
console = Console()
app = typer.Typer()


@app.command()
def set_root(path: Path):
    """
    set root path for projects and create environmet variable PROJECTS
    :return:
    """
    typer.echo(f"path received: {path}")



@app.command()
def update_root():
    """
    update root path for projects and create environmet variable PROJECTS
    :return:
    """
    pass

@app.command()
def create_project():
    """
    create project, set root path for project and environment variable PROJECT_ROOT
    create project confing.json for data
    structure: folder creation in PROJECT_ROOT
    /assets
    /shots
    /published
    /review
    /delivery
    /renders
    data:
    resolution: str "HD, 4K etc"
    fps: int "24, 23 etc"

    :return:
    project config.json should be created in PROJECT_ROOT folder
    """
    pass

@app.command()
def delete_project():
    """
    delete project, content and environments
    :return:
    """
    pass

@app.command()
def import_media():
    """
    import media and assets
    plates, assets, resources

    :return:
    """
    pass