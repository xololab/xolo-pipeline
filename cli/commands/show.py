import typer
from rich.console import Console
from rich.progress import track
from core import utils
import yaml
from typing import Optional

console = Console()
app = typer.Typer()

"""
Folder structure creation based on project type: VFX, ANIMATION, SHOT
"""

@app.command()
def create(
    project_name: str = typer.Option(..., prompt=True, confirmation_prompt=True),
    project_type: str = typer.Option(..., prompt=True, confirmation_prompt=True),
    resolution: str = typer.Option("", prompt="Resolution (e.g. 2048x858)", show_default=False),
    fps_input: str = typer.Option("", prompt="FPS (e.g. 24)", show_default=False)
):
    project_root = utils.config() / project_name
    project_root.mkdir(parents=True, exist_ok=True)
    console.print(f"[green]✔ Created project root: {project_root}[/green]")

    # Create folders
    folder_list = utils.project_types(project_type)
    for folder in track(folder_list, description="Processing..."):
        folder_path = project_root / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        console.print(f"[blue]├── {folder_path.relative_to(project_root)}[/blue]")

    # Load defaults from project_type
    project_info = utils.get_project_type_info(project_type)

    # Handle resolution
    if resolution:
        try:
            width, height = map(int, resolution.lower().split("x"))
            resolution_final = [width, height]
        except ValueError:
            console.print("[red]ERROR: Invalid resolution format. Use WIDTHxHEIGHT, e.g., 2048x858[/red]")
            raise typer.Exit(1)
    else:
        resolution_final = project_info.get("resolution")

    # Handle fps
    fps_final: Optional[float] = None
    if fps_input:
        try:
            fps_final = float(fps_input)
        except ValueError:
            console.print("[red]ERROR: Invalid FPS format. Please enter a number, e.g., 24[/red]")
            raise typer.Exit(1)
    else:
        fps_final = project_info.get("fps")


    # Build context
    context = {
        "project_name": project_name,
        "project_type": project_type,
        "resolution": resolution_final,
        "fps": fps_final,
        "ocio_config": project_info.get("ocio_config"),
        "paths": {
            folder: str((project_root / folder).resolve())
            for folder in folder_list
        } | {"root": str(project_root.resolve())}
    }

    context_path = project_root / "context.yaml"
    with open(context_path, "w") as f:
        yaml.dump(context, f, sort_keys=False)

    console.print(f"[green]✔ Created context.yaml at {context_path}[/green]")