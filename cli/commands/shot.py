import typer
from rich.console import Console
from rich.prompt import Prompt
from pathlib import Path
from typing import Optional
from core import utils

console = Console()
app = typer.Typer()

@app.command()
def create():
    """
    Create a shot manually with interactive project selection if not provided.
    """
    projects_root = utils.config()
    console.print(projects_root)

    selected_project = utils.select_project(projects_root)

    project_path = Path(projects_root) / selected_project


    context = utils.load_context(project_path)

    """
        sequence selection or creation
    """

    sequences_path = Path(context["paths"]["sequences"])

    existing_sequences = utils.list_sequences(sequences_path)

    console.print(f"[bold cyan]Existing Sequences:{existing_sequences}[/bold cyan]")
    for i, seq in enumerate(existing_sequences, start=1):
        console.print(f"{i}. {seq}")

    choice = Prompt.ask("Select a sequence or type a new one (e.g. 0000, seq01)")

    if choice.isdigit() and 1 <= int(choice) <= len(existing_sequences):
        sequence_name = existing_sequences[int(choice) - 1]
    else:
        sequence_name = choice
        (sequences_path / sequence_name).mkdir(parents=True, exist_ok=True)



    shot_id = Prompt.ask("Enter shot ID (e.g. 0010, 0020)")

    """
        creating shot structure to work in 
        
    """

    shot_path = sequences_path / sequence_name / shot_id


    if shot_path.exists():
        console.print(f"[red bold]Shot already exists:[/red bold]")
    else:
        utils.create_shot_structure(context, sequence_name, shot_id)




    console.print(f"[green]✔ Shot {sequence_name}_{shot_id} created in {context['project_name']}[/green]")