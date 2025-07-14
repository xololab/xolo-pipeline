import typer
from rich.console import Console

console = Console()
app = typer.Typer()


@app.command()
def create(
    sequence_name: str = typer.Option(
        "", prompt="sequence name (eg. seq01)", show_default=False
    ),
    shot_id: str = typer.Option(
        "", prompt="shot id (e.g. 0010, or 0020)", show_default=False)):


    if sequence_name:

        temp_name = [sequence_name, shot_id]

        shotname = "_".join(temp_name)
        console.print(f"[green]✔ Shot Created : {shotname}[/green]")
    else:
        shotname = shot_id
        console.print(f"[green]✔ Shot Created : {shotname}[/green]")
