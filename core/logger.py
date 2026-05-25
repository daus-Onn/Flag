import logging
import os
from datetime import datetime
from pathlib import Path
from rich.logging import RichHandler
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.table import Table
from rich import box

console = Console()

class Logger:
    _instance = None

    def __new__(cls, log_dir="outputs/logs"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, log_dir="outputs/logs"):
        if self._initialized:
            return
        self._initialized = True
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / f"flag_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        self.logger = logging.getLogger("FLAG")
        self.logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(file_format)
        self.logger.addHandler(file_handler)

        rich_handler = RichHandler(console=console, show_time=False, show_path=False, markup=True)
        rich_handler.setLevel(logging.INFO)
        self.logger.addHandler(rich_handler)

    def debug(self, msg): self.logger.debug(msg)
    def info(self, msg): self.logger.info(msg)
    def warning(self, msg): self.logger.warning(f"[yellow]{msg}[/yellow]")
    def error(self, msg): self.logger.error(f"[red]{msg}[/red]")
    def critical(self, msg): self.logger.critical(f"[bold red]{msg}[/bold red]")
    def success(self, msg): self.logger.info(f"[bold green]{msg}[/bold green]")

    @staticmethod
    def progress(description="Processing"):
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console,
            transient=False
        )

    @staticmethod
    def table(title="", columns=None, rows=None):
        if columns is None:
            columns = []
        if rows is None:
            rows = []
        table = Table(title=title, box=box.ROUNDED, border_style="cyan", header_style="bold cyan")
        for col in columns:
            table.add_column(col)
        for row in rows:
            table.add_row(*[str(c) for c in row])
        console.print(table)
        return table
