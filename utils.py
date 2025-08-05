import base64

from requests.auth import HTTPDigestAuth


class Util:

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
