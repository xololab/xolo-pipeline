import typer
import yaml
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt

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


def select_project(path: Path) -> Path:

    projects = []

    for p in path.iterdir():
        if p.is_dir():
            name = p.name
            projects.append(name)
            # projects.append(p)


    print("Available projects:")
    for i, p in enumerate(projects, start=1):
        print(f"{i}: {p}")
    idx = int(Prompt.ask("Select project by number"))
    return projects[idx - 1]



def load_context(project_path: Path) -> dict:
    context_file = project_path / "context.yaml"
    with open(context_file, "r") as f:
        return yaml.safe_load(f)


def list_sequences(sequences_path: Path):
    for p in sequences_path.iterdir():
        if p.is_dir():
            yield from list_sequences(p)



def create_shot_structure(context: dict, sequence: str, shot_id: str):
    base_path = Path(context["paths"]["sequences"]) / sequence / shot_id
    base_path.mkdir(parents=True, exist_ok=True)

    for folder in ["work", "publish"]:
        (base_path / folder).mkdir(parents=True, exist_ok=True)

    for dcc in ["maya", "nuke", "houdini", "gaffer"]:
        (base_path / "work" / dcc).mkdir(parents=True, exist_ok=True)