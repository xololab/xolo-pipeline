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
        "", prompt="shot id (e.g. 0010, or 0020)", show_default=False
    ),
):
    """

        shot command for create manually
    :param sequence_name:
    :param shot_id:
    :return:
    """
    console.print(f"[green]✔ Shot Created : {sequence_name}_{shot_id}[/green]")
