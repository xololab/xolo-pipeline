
import typer
from rich.console import Console
from rich.progress import track
from core import utils

console = Console()
app = typer.Typer()


@app.command()
def create(project_name: str = typer.Option(..., prompt=True, confirmation_prompt=True),
           project_type: str = typer.Option(..., prompt=True, confirmation_prompt=True)):

    project_root = utils.config() / project_name

    project_root.mkdir(parents=True, exist_ok=True)
    console.print(f"[green]✔ Created project root: {project_root}[/green]")


    for folder in track(utils.project_types(project_type), description="Processing..."):
        folder_path = project_root / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        console.print(f"[blue]├── {folder_path.relative_to(project_root)}[/blue]")






