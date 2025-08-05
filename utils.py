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
