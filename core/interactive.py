import cmd
import os
import subprocess
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich import box
from core.banner import Banner
from core.logger import Logger

console = Console()
logger = Logger()

class InteractiveMode(cmd.Cmd):
    intro = None
    prompt = "\033[36mFLAG> \033[0m"

    def __init__(self, modules):
        super().__init__()
        self.modules = modules
        self.current_module = None
        self.current_handler = None
        self.history = []
        self.verbose = False

    def preloop(self):
        console.clear()
        Banner.show()
        self._show_welcome()

    def _show_welcome(self):
        console.print("[bold yellow]Welcome to FLAG Interactive Mode![/bold yellow]")
        console.print("Type [bold cyan]help[/bold cyan] to see available commands.")
        console.print("Type [bold cyan]modules[/bold cyan] to list all modules.")
        console.print("Type a module name to select it (e.g. [bold cyan]forensic[/bold cyan])")
        console.print("Type [bold cyan]exit[/bold cyan] or [bold cyan]quit[/bold cyan] to leave.\n")

    def postcmd(self, stop, line):
        if self.current_module:
            self.prompt = f"\033[32mFLAG({self.current_module})> \033[0m"
        else:
            self.prompt = "\033[36mFLAG> \033[0m"
        return stop

    @staticmethod
    def _get_dest(flags):
        long_flags = [f for f in flags if f.startswith('--')]
        if long_flags:
            return long_flags[0][2:].replace('-', '_')
        return flags[0].lstrip('-').replace('-', '_')

    def do_modules(self, arg):
        table = Table(box=box.ROUNDED, border_style="cyan", header_style="bold cyan")
        table.add_column("Module", style="bold yellow")
        table.add_column("Description", style="white")
        table.add_column("Commands", style="green")

        for name, mod in self.modules.items():
            cmds = [c for c in mod.get_commands().keys() if not c.startswith("_")]
            desc = mod.get_commands().get("_description", name.capitalize() + " module")
            table.add_row(name, desc, ", ".join(cmds[:5]) + ("..." if len(cmds) > 5 else ""))

        console.print(table)

    def do_use(self, arg):
        if not arg:
            console.print("[red]Usage: use <module_name>[/red]")
            return
        if arg in self.modules:
            self.current_module = arg
            self.current_handler = self.modules[arg]
            console.print(f"[green]✓ Using module: {arg}[/green]")
            self._show_module_commands()
        else:
            console.print(f"[red]✗ Module '{arg}' not found. Type 'modules' to list.[/red]")

    def _show_module_commands(self):
        if not self.current_handler:
            return
        cmds = self.current_handler.get_commands()
        table = Table(box=box.SIMPLE, border_style="blue", header_style="bold blue")
        table.add_column("Command", style="bold yellow")
        table.add_column("Description", style="white")
        table.add_column("Usage", style="cyan")

        for name, info in cmds.items():
            if name.startswith("_"):
                continue
            usage = info.get("usage", "")
            desc = info.get("help", "")
            table.add_row(name, desc, usage)

        console.print(table)

    def do_run(self, arg):
        if not self.current_module:
            console.print("[red]No module selected. Use 'use <module>' first.[/red]")
            return
        if not arg:
            console.print("[red]Usage: run <command> [args][/red]")
            self._show_module_commands()
            return

        parts = arg.split()
        cmd_name = parts[0]
        cmd_args = parts[1:] if len(parts) > 1 else []

        cmds = self.current_handler.get_commands()
        if cmd_name not in cmds:
            console.print(f"[red]Unknown command '{cmd_name}' for module {self.current_module}[/red]")
            return

        handler = cmds[cmd_name].get("handler")
        if not handler:
            console.print(f"[red]No handler for '{cmd_name}'[/red]")
            return

        console.print(f"[cyan]Running: {self.current_module} {cmd_name} {' '.join(cmd_args)}[/cyan]")

        class FakeArgs:
            pass

        fake_args = FakeArgs()
        fake_args.command = cmd_name

        arg_defs = cmds[cmd_name].get("args", [])
        positional_idx = 0
        i = 0
        while i < len(cmd_args):
            token = cmd_args[i]
            matched = False
            for arg_info in arg_defs:
                flags = arg_info.get("flags", [])
                if token in flags:
                    dest = arg_info.get("dest") or self._get_dest(flags)
                    if arg_info.get("action") in ("store_true", "store_false"):
                        setattr(fake_args, dest, arg_info.get("action") == "store_true")
                        matched = True
                        i += 1
                        break
                    else:
                        if i + 1 < len(cmd_args):
                            val = cmd_args[i + 1].strip('"\'')
                            if arg_info.get("type") == int:
                                try:
                                    val = int(val)
                                except:
                                    pass
                            setattr(fake_args, dest, val)
                            matched = True
                            i += 2
                            break
            if not matched:
                for arg_info in arg_defs:
                    flags = arg_info.get("flags", [])
                    is_positional = all(f.startswith('-') for f in flags) == False
                    if is_positional:
                        dest = arg_info.get("dest") or self._get_dest(flags)
                        if not hasattr(fake_args, dest):
                            val = token.strip('"\'')
                            if arg_info.get("type") == int:
                                try:
                                    val = int(val)
                                except:
                                    pass
                            setattr(fake_args, dest, val)
                            matched = True
                            i += 1
                            break
            if not matched:
                i += 1

        for arg_info in arg_defs:
            flags = arg_info.get("flags", [])
            dest = arg_info.get("dest") or self._get_dest(flags)
            if not hasattr(fake_args, dest):
                if arg_info.get("action") == "store_true":
                    setattr(fake_args, dest, False)
                elif arg_info.get("action") == "store_false":
                    setattr(fake_args, dest, True)
                else:
                    setattr(fake_args, dest, arg_info.get("default", None))

        try:
            result = handler(fake_args)
            if result and self.verbose:
                console.print(f"\n[dim]Result: {result}[/dim]")
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")

    def do_show(self, arg):
        if not self.current_module:
            console.print("[red]No module selected.[/red]")
            return
        if arg == "commands":
            self._show_module_commands()
        elif arg == "info":
            console.print(f"[yellow]Current Module:[/yellow] {self.current_module}")
            console.print(f"[yellow]Commands:[/yellow] {len(self.current_handler.get_commands())}")
        else:
            console.print(f"[red]Unknown: show {arg}[/red]")

    def do_verbose(self, arg):
        self.verbose = not self.verbose
        console.print(f"[green]Verbose mode: {'ON' if self.verbose else 'OFF'}[/green]")

    def do_clear(self, arg):
        console.clear()
        Banner.show()

    def do_EOF(self, arg):
        return True

    def do_exit(self, arg):
        console.print("[yellow]Goodbye![/yellow]")
        return True

    def do_quit(self, arg):
        return self.do_exit(arg)

    def do_help(self, arg):
        if arg:
            if self.current_module:
                cmds = self.current_handler.get_commands()
                if arg in cmds:
                    info = cmds[arg]
                    console.print(f"[bold yellow]Command:[/bold yellow] {arg}")
                    console.print(f"[bold yellow]Help:[/bold yellow] {info.get('help', 'N/A')}")
                    console.print(f"[bold yellow]Usage:[/bold yellow] {info.get('usage', 'N/A')}")
                    return
            console.print(f"[red]No help for '{arg}'[/red]")
            return

        console.print("[bold cyan]FLAG Commands:[/bold cyan]")
        console.print("  [bold yellow]modules[/bold yellow]            - List available modules")
        console.print("  [bold yellow]use <module>[/bold yellow]      - Select a module to use")
        console.print("  [bold yellow]run <cmd> [args][/bold yellow] - Run a module command")
        console.print("  [bold yellow]show commands[/bold yellow]     - Show current module commands")
        console.print("  [bold yellow]show info[/bold yellow]         - Show current module info")
        console.print("  [bold yellow]verbose[/bold yellow]           - Toggle verbose mode")
        console.print("  [bold yellow]clear[/bold yellow]             - Clear screen")
        console.print("  [bold yellow]help[/bold yellow]              - Show this help")
        console.print("  [bold yellow]exit/quit[/bold yellow]         - Exit FLAG")
        console.print("[bold cyan]Shell Commands:[/bold cyan]")
        console.print("  [bold yellow]ls[/bold yellow], [bold yellow]pwd[/bold yellow], [bold yellow]cd <dir>[/bold yellow] - Run system commands directly")

    def default(self, line):
        if ' ' in line:
            parts = line.split()
            cmd = parts[0]
            rest = ' '.join(parts[1:])
            if self.current_module:
                cmds = self.current_handler.get_commands()
                if cmd in cmds:
                    self.do_run(line)
                    return
                elif cmd in self.modules:
                    self.do_use(cmd)
                    if rest:
                        self.do_run(rest)
                    return
            elif cmd in self.modules:
                self.do_use(cmd)
                if rest:
                    self.do_run(rest)
                return
        elif line in self.modules:
            self.do_use(line)
            return

        try:
            if line.strip().startswith('cd '):
                path = line.strip()[3:].strip()
                target = Path(path).expanduser().resolve()
                os.chdir(target)
                console.print(f"[dim]→ {Path.cwd()}[/dim]")
            else:
                result = subprocess.run(line, shell=True, capture_output=True, text=True, timeout=30)
                if result.stdout:
                    console.print(result.stdout.rstrip())
                if result.stderr:
                    console.print(f"[red]{result.stderr.rstrip()}[/red]")
                if result.returncode != 0 and not result.stdout:
                    console.print(f"[red]Command failed: {line}[/red]")
        except FileNotFoundError:
            console.print(f"[red]Command not found: {line}[/red]")
        except subprocess.TimeoutExpired:
            console.print(f"[red]Command timed out: {line}[/red]")
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")

    def emptyline(self):
        pass
