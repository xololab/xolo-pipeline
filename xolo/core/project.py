import typer
from rich.console import Console
from rich.table import Table
from pathlib import Path
import yaml
from .models import ProjectData, FolderStructure
from rich.progress import track



console = Console()
app = typer.Typer()


@app.command()
def set_root(path: Path):
    """
    Set root path for projects and create environment variable PROJECTS
    """
    project_root = path
    config_data = {"PROJECTS": str(project_root)}
    config_path = Path(__file__).resolve().parent.parent.parent / "config.yaml"
    with config_path.open("w") as f:
        yaml.dump(config_data, f, default_flow_style=False)
    typer.echo(f"Path saved to config.yaml: {project_root}")




@app.command()
def update_root(path: Path):
    """
    update root path for projects and create environmet variable PROJECTS

    """
    pass

@app.command()
def create_project(project_name: str):
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


    project config.json should be created in PROJECT_ROOT folder
    """
    config_path = Path(__file__).resolve().parent.parent.parent / "config.yaml"

    if config_path.exists():
        with config_path.open("r") as f:
            config = yaml.safe_load(f)
        root_path = Path(config["PROJECTS"])
        structure = FolderStructure()
        for _, rel_path in track(structure.model_dump().items(), description="Creating project"):

            folder_path = root_path / project_name / rel_path.lstrip("/")
            folder_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 Created: {folder_path}")

    else:
        typer.secho("config file not found", fg=typer.colors.RED)




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