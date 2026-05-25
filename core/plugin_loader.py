import importlib
import inspect
import os
import sys
from pathlib import Path
from rich.console import Console

console = Console()

class PluginLoader:
    def __init__(self, plugin_dir="plugins"):
        self.plugin_dir = Path(plugin_dir)
        self.plugins = {}
        self.plugin_dir.mkdir(exist_ok=True)
        self._init_plugin_dir()

    def _init_plugin_dir(self):
        init_file = self.plugin_dir / "__init__.py"
        if not init_file.exists():
            init_file.write_text("")

    def discover_plugins(self):
        self.plugins = {}
        if not self.plugin_dir.exists():
            return self.plugins

        sys.path.insert(0, str(self.plugin_dir.parent))

        for file in self.plugin_dir.glob("*.py"):
            if file.name == "__init__.py":
                continue
            try:
                spec = importlib.util.spec_from_file_location(
                    f"plugins.{file.stem}", file
                )
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    plugin_name = file.stem
                    self.plugins[plugin_name] = module
                    console.print(f"[dim]Loaded plugin: {plugin_name}[/dim]")
            except Exception as e:
                console.print(f"[red]Failed to load plugin {file.name}: {e}[/red]")

        sys.path.pop(0)
        return self.plugins

    def get_plugin(self, name):
        return self.plugins.get(name)

    def list_plugins(self):
        return list(self.plugins.keys())

    def reload_plugins(self):
        self.plugins = {}
        return self.discover_plugins()
