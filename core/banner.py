from rich.console import Console
from rich.text import Text

console = Console()

class Banner:
    @staticmethod
    def show():
        lines = [
            ("[bold cyan]************************************************************", ""),
            ("[bold cyan]*                                                          *", ""),
            ("[bold cyan]*                      [/bold cyan][bold red]*** FLAG ***[/bold red][bold cyan]                        *", ""),
            ("[bold cyan]*      [/bold cyan][bold green]Framework CLI Cybersecurity for CTF & Learning[/bold green][bold cyan]      *", ""),
            ("[bold cyan]*      [/bold cyan][bold yellow]Forensics[/bold yellow] - [bold yellow]Crypto[/bold yellow] - [bold yellow]PWN[/bold yellow] - [bold yellow]Reverse Engineering[/bold yellow][bold cyan]      *", ""),
            ("[bold cyan]*               [/bold cyan][bold blue]https://github.com/YogaRmdn[/bold blue][bold cyan]                *", ""),
            ("[bold cyan]*                                                          *", ""),
            ("[bold cyan]************************************************************", ""),
        ]
        for line, _ in lines:
            console.print(line)

    @staticmethod
    def show_help():
        help_text = """
[bold cyan]USAGE:[/bold cyan]
    [green]python main.py [module] [command] [options][/green]

[bold cyan]MODULES:[/bold cyan]
    [bold yellow]forensic[/bold yellow]    - Forensics analysis tools
    [bold yellow]crypto[/bold yellow]      - Cryptography tools
    [bold yellow]pwn[/bold yellow]         - Binary exploitation tools
    [bold yellow]reverse[/bold yellow]     - Reverse engineering tools

[bold cyan]EXAMPLES:[/bold cyan]
    python main.py crypto base64 -d SGVsbG8=
    python main.py forensic metadata image.jpg
    python main.py pwn pattern 500
    python main.py reverse pe malware.exe
    python main.py                      - Interactive mode

[bold cyan]GLOBAL OPTIONS:[/bold cyan]
    -o, --output FILE    Save output to file (TXT/JSON)
    -v, --verbose        Verbose output
    --help               Show this help message
        """
        console.print(help_text)

    @staticmethod
    def show_about():
        about_text = """
[bold cyan]FLAG - Framework Learning and Analysis for Cybersecurity[/bold cyan]

Version  : 2.0
Author   : Flag Team
Purpose  : Educational CTF & Cybersecurity learning platform
Modules  : Forensics, Crypto, Binary Exploitation (PWN), Reverse Engineering

[bold yellow]DISCLAIMER:[/bold yellow]
This tool is intended for educational purposes, CTF competitions,
and authorized security testing only. Users are responsible for
complying with all applicable laws and regulations.

[bold green]Happy Hacking![/bold green]
        """
        console.print(about_text)
