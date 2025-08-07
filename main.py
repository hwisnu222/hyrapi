from rich.text import Text
import typer
from client import Client
from InquirerPy import inquirer
from rich import print
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import Terminal256Formatter
from rich.console import Console
import json

from utils import Util

app = typer.Typer()


@app.command()
def main(
    config: str = typer.Option(..., "--collection", "-c", help="YAML request file"),
    env: str = typer.Option(None, "--environment", "-e", help="environment server"),
    request_name: str = typer.Option(None, "--name", "-n", help="request name"),
    show_servers: bool = typer.Option(
        False, "--servers", "-s", is_flag=True, help="show list server"
    ),
    show_paths: bool = typer.Option(
        False, "--paths", "-p", is_flag=True, help="Show all paths"
    ),
    quiet: bool = typer.Option(
        False, "--quiet", "-q", is_flag=True, help="quiet response"
    ),
):
    util = Util()

    try:
        data = util.load_config(config, env)[0]
    except Exception as e:
        typer.echo(f"Failed to collection: {e}")
        raise typer.Exit()

    # generate list of choices
    choices = []
    paths = data.get("paths")

    if not paths:
        typer.echo("there is not paths on collection")
        raise typer.Exit()

    if not data.get("servers"):
        typer.echo("Please set server to collection")
        raise typer.Exit()

    # get servers
    servers = data.get("servers", [])
    index_env = next(
        (i for i, server in enumerate(servers) if server["name"] == env), 0
    )
    if show_servers:
        util.dict_to_table(servers)
        raise typer.Exit()

    if show_paths:
        util.dict_to_table(paths)
        raise typer.Exit()

    for i, req in enumerate(paths):
        method = req.get("method", "GET").upper()
        name = req.get("name", "unknown-name")
        endpoint = req.get("endpoint", "-")
        label = f"[{method}] {name} {endpoint}"
        choices.append({"name": label, "value": i})

    if request_name:
        index = next(
            (i for i, item in enumerate(paths) if item["name"] == request_name), -1
        )
        if index == -1:
            typer.echo("request name is not found")
            raise typer.Exit()

    else:
        index = inquirer.fuzzy(
            message=f"Select a request to send({servers[index_env]["name"]}):",
            choices=choices,
            instruction="(type to filter, ↑↓ to select)",
        ).execute()

    path = paths[index]
    client = Client(path, data)

    try:
        response = client.send(index_env)
        try:

            console = Console()
            if not quiet:
                for key, value in response.headers.items():
                    print(f"[green]{key}[/green]: [white]{value}[/white]")

                print(
                    f"\nRequest: {util.safe_join(servers[index_env]['url'], path['endpoint'])}\n"
                    f"Method: {path['method']}\n"
                    f"[bold]Status:[/bold] [cyan]{response.status_code}-{response.reason}[/cyan] "
                    f"[bold]Time:[/bold] [cyan]{response.elapsed.total_seconds():.3f}s[/cyan] "
                    f"[bold]Size:[/bold] [cyan]{util.format_size(len(response.content))}[/cyan]\n\n"
                    f"[grey]Response[/grey]"
                )

            # formatter response
            json_str = json.dumps(response.json(), indent=2)

            highlighted = highlight(
                json_str, JsonLexer(), Terminal256Formatter(style="solarized-dark")
            )

            text = Text.from_ansi(highlighted, overflow="fold", no_wrap=False)
            console.print(text)
        except:
            typer.echo(response.text)
    except Exception as e:
        typer.echo(f"Request failed: {e}")


if __name__ == "__main__":
    app()
