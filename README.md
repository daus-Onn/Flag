# FLAG - Framework Learning and Analysis for Cybersecurity

A modular CLI cybersecurity framework for CTF competitions and cybersecurity learning with interactive and command-line modes.

## Features

- **4 Core Modules**: Forensics, Cryptography, Binary Exploitation (PWN), Reverse Engineering
- **Dual Mode**: CLI command-line mode + Interactive REPL mode with auto-completion
- **Rich Terminal UI**: Colored output, tables, progress bars, spinners
- **Plugin System**: Auto-loads Python plugins from `plugins/` directory
- **Output Export**: Save results to TXT or JSON with `-o` flag
- **Logging**: Timestamped logs saved to `outputs/logs/`
- **Configurable**: Settings via `settings.json`
- **Shell Commands**: Run system commands directly in interactive mode (ls, pwd, cd)

## Installation

### Quick Install
```bash
pip install -r requirements.txt

# Optional extras per module:
pip install Pillow yara-python scapy binwalk        # Forensics
pip install pycryptodome                              # Crypto
pip install pwntools capstone                         # PWN
pip install pefile pyelftools capstone                # Reverse
```

## Usage

### CLI Mode
```bash
python flag.py <module> <command> [options]
```

### Interactive Mode
```bash
python flag.py
```

### Global Options
| Option | Description |
|--------|-------------|
| `-o, --output FILE` | Save output to TXT/JSON |
| `-v, --verbose` | Enable verbose output |

## Modules

### Forensics (`forensic`)
| Command | Description |
|---------|-------------|
| `metadata <file>` | Extract file metadata (size, timestamps, permissions) |
| `exif <image>` | Extract EXIF data from images (requires Pillow) |
| `strings <file> -n 4` | Extract printable strings from file |
| `hidden <file>` | Detect hidden/appended/embedded files |
| `entropy <file>` | Calculate file entropy with analysis |
| `signature <file>` | Check file magic bytes/signatures (40+ formats) |
| `yara <file> -r rules.yar` | Scan with YARA rules (requires yara-python) |
| `zip <archive>` | Analyze ZIP file structure |
| `pcap <file>` | PCAP network analysis (requires scapy) |
| `binwalk <file>` | Scan for embedded files (requires binwalk) |
| `all <file>` | Run all applicable forensics analyses |

### Cryptography (`crypto`)
| Command | Description |
|---------|-------------|
| `base64 -e/-d <data>` | Base64 encode/decode |
| `hex -e/-d <data>` | Hex encode/decode |
| `rot13 <text>` | ROT13 cipher |
| `caesar <text> <shift>` | Caesar cipher with all-shifts view |
| `xor <data> <key>` | XOR encrypt/decrypt |
| `aes -e/-d <data> <key>` | AES-CBC encrypt/decrypt (requires pycryptodome) |
| `hash <data> -a sha256` | Generate hash (md5, sha1, sha256, sha512, blake2, sha3) |
| `hashid <hash>` | Identify hash type by length/format |
| `crack <hash> <wordlist> -a md5` | Dictionary hash cracker with progress bar |
| `freq <text>` | Frequency analysis with IoC (Index of Coincidence) |

### Binary Exploitation (`pwn`)
| Command | Description |
|---------|-------------|
| `pattern <length>` | Generate cyclic pattern (requires pwntools) |
| `offset <value>` | Find cyclic offset in pattern |
| `elf <binary>` | Parse ELF binary analysis |
| `rop <binary> -g "pop rdi"` | Find ROP gadgets (requires pwntools) |
| `shellcode execve -a amd64` | Generate shellcode (execve, reverse, bind) |
| `template <binary>` | Generate pwntools exploit template |
| `checksec <binary>` | Check security features (RELRO, Canary, NX, PIE) |
| `asm "xor eax, eax" -a i386` | Assemble instructions to bytes (requires pwntools) |

### Reverse Engineering (`reverse`)
| Command | Description |
|---------|-------------|
| `pe <file>` | Analyze PE file (requires pefile) |
| `elf <file>` | Analyze ELF binary (requires pyelftools) |
| `strings <file> -n 5` | Extract strings from binary |
| `disasm <file> -s .text -c 100` | Disassemble binary (requires capstone) |
| `opcode <file>` | View opcode statistics |
| `sections <file>` | Analyze binary sections |
| `imports <file>` | View imported functions |
| `exports <file>` | View exported functions |
| `packer <file>` | Detect packers/obfuscators |
| `all <file>` | Run all reverse analyses |

## Interactive Mode Usage

```
$ python main.py

  **** ... FLAG banner ... ****

FLAG> help
FLAG> modules
FLAG> use forensic
FLAG(forensic)> run metadata image.jpg
FLAG(forensic)> run strings suspicious.bin -n 8
FLAG> exit
```

Interactive commands: `modules`, `use <module>`, `run <cmd> [args]`, `show commands`, `show info`, `verbose`, `clear`, `help`, `exit`/`quit`. Shell commands (ls, pwd, cd) also work directly.

## Plugin System

Create `plugins/my_plugin.py`:
```python
from rich.console import Console
console = Console()

def register():
    return {"name": "my_plugin", "description": "My plugin", "version": "1.0"}

def run(args):
    console.print(f"[green]Plugin executed with: {args}[/green]")
```

## Configuration

Edit `settings.json` to customize theme colors, output directory, logging, and module settings.

## Project Structure

```
FLAG/
├── flag.py                    # Entry point
├── settings.json              # Configuration
├── requirements.txt           # Dependencies
├── core/
│   ├── banner.py              # ASCII banner & display
│   ├── config.py              # Configuration manager
│   ├── logger.py              # Logging system (file + console)
│   ├── base.py                # Base module class
│   ├── interactive.py         # Interactive REPL mode
│   └── plugin_loader.py       # Plugin discovery
├── modules/
│   ├── forensics/forensics.py # Forensics module
│   ├── crypto/crypto.py       # Crypto module
│   ├── pwn/pwn.py             # PWN module
│   └── reverse/reverse.py     # Reverse module
├── outputs/logs/              # Timestamped logs
├── plugins/                   # User plugins (auto-loaded)
└── wordlists/                 # Wordlists directory
```

## Disclaimer

> **⚠️ For educational purposes, CTF competitions, and authorized security testing only.**
> Do not use on systems you do not own or have explicit permission to test.
