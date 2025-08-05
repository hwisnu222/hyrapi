from rich.text import Text
import typer
from model import load_config
from client import Client
from InquirerPy import inquirer
from rich import print
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
from rich.console import Console
import json

from utils import Util

app = typer.Typer()


@app.command()
def main(
    config: str = typer.Option(..., "--collection", "-c", help="YAML request file"),
):
    util = Util()

    try:
        data = load_config(config)[0]
    except Exception as e:
        typer.echo(f"Failed to collection: {e}")
        raise typer.Exit()

    # generate list of choices
    choices = []
    paths = data.get("paths")
    for i, req in enumerate(paths):
        method = req.get("method", "GET").upper()
        name = req.get("name", "unknown-name")
        endpoint = req.get("endpoint", "-")
        label = f"[{method}] {name} {endpoint}"
        choices.append({"name": label, "value": i})

    index = inquirer.fuzzy(
        message="Select a request to send:",
        choices=choices,
        instruction="(Use arrow keys or search)",
    ).execute()

    path = paths[index]
    client = Client(path, data)

    try:
        response = client.send()
        try:
            typer.echo("----------------------------------")
            for key, value in response.headers.items():
                print(f"[green]{key}[/green]: [white]{value}[/white]")
            typer.echo("----------------------------------\n")
            print(
                f"[bold]Status:[/bold] [cyan]{response.status_code}-{response.reason}[/cyan] [bold]Time:[/bold] [cyan]{response.elapsed.total_seconds():.3f}s[/cyan] [bold]Size:[/bold] [cyan]{util.format_size(len(response.content))}[/cyan]"
            )

            json_str = json.dumps(response.json(), indent=2)

            highlighted = highlight(json_str, JsonLexer(), TerminalFormatter())

            text = Text.from_ansi(highlighted, overflow="fold", no_wrap=False)
            console = Console()
            print("[grey]Response[/grey]")
            console.print(text)
        except:
            typer.echo(response.text)
    except Exception as e:
        typer.echo(f"Request failed: {e}")


if __name__ == "__main__":
    app()
