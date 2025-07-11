
import typer
from typing_extensions import Annotated
from rich.console import Console
from pathlib import Path
import os
import yaml


console = Console()
app = typer.Typer()




@app.command()
def test():
    console.print("[blue underline]test done")


@app.command()
def projects_directory(projects: Path = typer.Option(..., prompt=True, confirmation_prompt=True),
                       assets: Path = typer.Option(..., prompt=True, confirmation_prompt=True)):
    """
        Set roots path for projects and  global assets folders create environment variable PROJECTS, GLOBAL_ASSETS, and
        USERNAME.
    """
    project_root = projects
    assets_root = assets
    username = os.getlogin()
    config_data = {"PROJECTS": str(project_root), "GLOBAL_ASSETS": str(assets_root), "USERNAME": username}
    config_path = Path(__file__).resolve().parent.parent.parent / "config.yaml"
    with config_path.open("w") as f:
        yaml.dump(config_data, f, default_flow_style=False)
    typer.echo(f"Path saved to config.yaml: {project_root}")

    if config_path.exists():
        with config_path.open("r") as f:
            config = yaml.safe_load(f)
        projects_path = Path(config["PROJECTS"])
        assets_path = Path(config["GLOBAL_ASSETS"])
        user = Path(config["USERNAME"])
        os.environ["PROJECTS"] = str(projects_path)
        os.environ["GLOBAL_ASSETS"] = str(assets_path)
        projects_env = os.getenv("PROJECTS")
        global_assets_env = os.getenv("GLOBAL_ASSETS")
        console.log(f'PROJECTS env: {projects_env}', style="blue")
        console.log(f"Global_ASSETS env: {global_assets_env}", style="blue")
        console.print(f'current USERNAME: {user}', style="red")
    else:
        console.print("Environment variable PROJECTS and GLOBAL_ASSETS not set", style="red")


