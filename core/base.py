import json
import os
from pathlib import Path
from abc import ABC, abstractmethod
from rich.console import Console
from core.logger import Logger

console = Console()
logger = Logger()

class BaseModule(ABC):
    def __init__(self):
        self.name = self.__class__.__name__
        self.logger = logger
        self.console = console

    @abstractmethod
    def get_commands(self):
        return {}

    def register_commands(self, parser):
        subparsers = parser.add_subparsers(dest="command", help=f"{self.name} commands")
        for cmd_name, cmd_info in self.get_commands().items():
            if cmd_name.startswith("_"):
                continue
            cmd_parser = subparsers.add_parser(cmd_name, help=cmd_info.get("help", ""))
            for arg in cmd_info.get("args", []):
                flags = arg.get("flags", [])
                kwargs = {k: v for k, v in arg.items() if k != "flags"}
                cmd_parser.add_argument(*flags, **kwargs)

    def handle(self, args):
        commands = self.get_commands()
        if args.command in commands:
            handler = commands[args.command].get("handler")
            if handler:
                try:
                    result = handler(args)
                    self._handle_output(result, args)
                except Exception as e:
                    self.logger.error(f"{self.name} Error: {str(e)}")
                    console.print(f"\n[red]✗ Error: {str(e)}[/red]")
        else:
            console.print(f"[red]✗ Unknown command: {args.command}[/red]")

    def _handle_output(self, data, args):
        if data is None:
            return

        output_file = getattr(args, 'output', None)
        if output_file:
            ext = Path(output_file).suffix.lower()
            try:
                if ext == '.json':
                    with open(output_file, 'w') as f:
                        json.dump(data, f, indent=2, default=str)
                else:
                    with open(output_file, 'w') as f:
                        if isinstance(data, str):
                            f.write(data)
                        else:
                            f.write(json.dumps(data, indent=2, default=str))
                console.print(f"\n[green]✓ Output saved to: {output_file}[/green]")
            except Exception as e:
                console.print(f"[red]✗ Failed to save output: {e}[/red]")

    def save_text(self, filename, content):
        output_dir = Path.cwd() / "outputs"
        output_dir.mkdir(parents=True, exist_ok=True)
        filepath = output_dir / filename
        with open(filepath, 'w') as f:
            f.write(str(content))
        return filepath

    @staticmethod
    def read_file(path):
        with open(path, 'rb') as f:
            return f.read()

    @staticmethod
    def read_text(path):
        with open(path, 'r', errors='ignore') as f:
            return f.read()
