import base64
from rich.console import Console
from rich.table import Table
import yaml
from pathlib import Path
from typing import List, Union
from jinja2 import Template
from requests.auth import HTTPDigestAuth


class Util:
    def safe_join(self, base: str, path: str) -> str:
        return base.rstrip("/") + "/" + path.lstrip("/")

    def load_config(self, file_path: Union[str, Path], env: str) -> List[dict]:
        util = Util()

        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if file_path.suffix not in [".yaml", ".yml"]:
            raise ValueError("Unsupported file format. Use .yaml or .yml")

        # Read and render template first
        raw_text = file_path.read_text()
        parsed_yaml = yaml.safe_load(raw_text)
        variables = parsed_yaml.get("variables", {})
        global_variables = util.filter_variables(variables=variables)
        env_variables = variables.get(env, {})

        template = Template(raw_text)
        rendered_yaml = template.render(**{**global_variables, **env_variables})

        # Load rendered YAML
        config = yaml.safe_load(rendered_yaml)

        if isinstance(config, dict):
            return [config]
        elif isinstance(config, list):
            return config
        else:
            raise ValueError("Config must be a dict or list of dicts")

    def dict_to_table(self, data):
        console = Console()
        table = Table(show_header=True, header_style="bold green")

        # headers
        for key in data[0].keys():
            table.add_column(key)

        # rows
        for item in data:
            row = [str(item.get(key, "")) for key in data[0].keys()]
            table.add_row(*row)

        console.print(table)

    def filter_variables(self, variables={}):
        filtered = {
            k: v for k, v in variables.items() if isinstance(v, (str, int, float))
        }
        return filtered

    def format_size(self, size_bytes: int) -> str:
        if size_bytes < 1024:
            return f"[bold cyan]{size_bytes} B[/bold cyan]"
        elif size_bytes < 1024**2:
            return f"[bold green]{size_bytes / 1024:.2f} KB[/bold green]"
        elif size_bytes < 1024**3:
            return f"[bold yellow]{size_bytes / (1024 ** 2):.2f} MB[/bold yellow]"
        else:
            return f"[bold red]{size_bytes / (1024 ** 3):.2f} GB[/bold red]"

    def load_auth_header(self, auth):
        auth_type = auth.get("type")

        if auth_type == "basic":
            user = auth.get("username")
            password = auth.get("password")
            encoded = base64.b64encode(f"{user}:{password}".encode()).decode()

            return {"Authorization": f"Basic {encoded}"}, None

        elif auth_type == "bearer":
            token = auth.get("token")
            return {"Authorization": f"Bearer {token}"}, None

        elif auth_type == "apikey":
            key = auth.get("api_key")
            header_name = auth.get("api_key_header", "X-API-Key")
            return {header_name: key}, None

        elif auth_type == "digest":
            return {}, HTTPDigestAuth(auth.get("username"), auth.get("password"))

        return {}, None
