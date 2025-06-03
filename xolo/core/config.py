import typer
from rich.console import Console
from rich.table import Table
from pathlib import Path
import yaml
from .models import ProjectData, FolderStructure
from rich.progress import track
import os

console = Console()
app = typer.Typer()

@app.command()
def set_roots(projects: Path, assets: Path):
    """
    Set roots path for projects and  global assets folders create environment variable PROJECTS and GLOBAL_ASSETS
    """
    project_root = projects
    assets_root = assets
    config_data = {"PROJECTS": str(project_root), "GLOBAL_ASSETS": str(assets_root)}
    config_path = Path(__file__).resolve().parent.parent.parent / "config.yaml"
    with config_path.open("w") as f:
        yaml.dump(config_data, f, default_flow_style=False)
    typer.echo(f"Path saved to config.yaml: {project_root}")

    if config_path.exists():
        with config_path.open("r") as f:
            config = yaml.safe_load(f)
        projects_path = Path(config["PROJECTS"])
        assets_path = Path(config["GLOBAL_ASSETS"])
        os.environ["PROJECTS"] = str(projects_path)
        os.environ["GLOBAL_ASSETS"] = str(assets_path)
    else:
        typer.echo("Environment variable PROJECTS and GLOBAL_ASSETS not set", fg=typer.colors.RED)





@app.command()
def update_roots(path: Path):
    """
    update root path for projects and global assets  and create environment variable PROJECTS

    """
    pass
