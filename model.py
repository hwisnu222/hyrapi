import yaml
from pathlib import Path
from typing import List, Union
from jinja2 import Template


def load_config(file_path: Union[str, Path]) -> List[dict]:
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.suffix not in [".yaml", ".yml"]:
        raise ValueError("Unsupported file format. Use .yaml or .yml")

    # Read and render template first
    raw_text = file_path.read_text()
    parsed_yaml = yaml.safe_load(raw_text)
    variables = parsed_yaml.get("variables", {})

    template = Template(raw_text)
    rendered_yaml = template.render(**variables)

    # Load rendered YAML
    config = yaml.safe_load(rendered_yaml)

    if isinstance(config, dict):
        return [config]
    elif isinstance(config, list):
        return config
    else:
        raise ValueError("Config must be a dict or list of dicts")
