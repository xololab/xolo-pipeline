import typer
import yaml
from pathlib import Path
from rich.console import Console

console = Console()

# Constants
ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config.yaml"
PROJECT_STRUCTURE = ROOT / "core" / "templates" / "project_type.yaml"



# ymal loaders

def config() -> Path:
    if not CONFIG.exists():
        console.print("[red]ERROR: config.yaml not found.[/red]")
        raise typer.Exit(1)

    with open(CONFIG, "r") as f:
        data = yaml.safe_load(f)

    projects_root = Path(data.get("PROJECTS", ""))
    if not projects_root.exists():
        console.print(f"[red]ERROR: Configured PROJECTS path does not exist: {projects_root}[/red]")
        raise typer.Exit(1)

    return projects_root

def project_types(project_type: str) -> list:
    if not PROJECT_STRUCTURE.exists():
        console.print("[red]ERROR: project_type.yaml not found.[/red]")
        raise typer.Exit(1)

    with open(PROJECT_STRUCTURE, "r") as f:
        types = yaml.safe_load(f)

    if project_type not in types:
        console.print(f"[red]ERROR: Project type '{project_type}' not found in project_type.yaml[/red]")
        raise typer.Exit(1)

    return types[project_type].get("default_folders", [])



def get_project_type_info(project_type: str) -> dict:
    if not PROJECT_STRUCTURE.exists():
        console.print("[red]ERROR: project_type.yaml not found.[/red]")
        raise typer.Exit(1)

    with open(PROJECT_STRUCTURE, "r") as f:
        types = yaml.safe_load(f)

    if project_type not in types:
        console.print(f"[red]ERROR: Project type '{project_type}' not found in project_type.yaml[/red]")
        raise typer.Exit(1)

    return types[project_type]
