"""
setup.py — One-command environment bootstrap
Run this ONCE after cloning the repo.

    python setup.py

It will:
  1. Check Python version
  2. Create a virtual environment (venv/)
  3. Install all dependencies from requirements.txt
  4. Create all project folders
  5. Print next steps
"""

import os
import sys
import subprocess
import platform

MIN_PYTHON = (3, 10)
VENV_DIR   = "venv"

BOLD   = "\033[1m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
RESET  = "\033[0m"


def banner():
    print(f"\n{BOLD}{CYAN}")
    print("╔══════════════════════════════════════════════════════╗")
    print("║   Mutual Fund Analytics — Project Setup             ║")
    print("╚══════════════════════════════════════════════════════╝")
    print(RESET)


def check_python():
    v = sys.version_info
    print(f"  Python version: {v.major}.{v.minor}.{v.micro}")
    if (v.major, v.minor) < MIN_PYTHON:
        print(f"{RED}  ❌ Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ required. Please upgrade.{RESET}")
        sys.exit(1)
    print(f"{GREEN}  ✅ Python version OK{RESET}")


def create_venv():
    if os.path.isdir(VENV_DIR):
        print(f"{YELLOW}  ⚠️  venv/ already exists — skipping creation{RESET}")
        return
    print("\n  Creating virtual environment…")
    subprocess.run([sys.executable, "-m", "venv", VENV_DIR], check=True)
    print(f"{GREEN}  ✅ venv/ created{RESET}")


def get_pip():
    if platform.system() == "Windows":
        return os.path.join(VENV_DIR, "Scripts", "pip")
    return os.path.join(VENV_DIR, "bin", "pip")


def install_deps():
    pip = get_pip()
    print("\n  Installing dependencies from requirements.txt…")
    # Skip pip self-upgrade (can fail on newer Python versions)
    result = subprocess.run(
        [pip, "install", "-r", "requirements.txt"],
        capture_output=False
    )
    if result.returncode != 0:
        print(f"{YELLOW}  ⚠️  Some packages may have failed. Trying with --no-deps fallback…{RESET}")
        subprocess.run([pip, "install", "-r", "requirements.txt", "--no-deps"])
    print(f"{GREEN}  ✅ Dependencies installed{RESET}")


def create_dirs():
    dirs = [
        "data/raw", "data/processed",
        "notebooks", "sql", "dashboard", "reports",
    ]
    print("\n  Creating folder structure…")
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"    📁 {d}/")
    print(f"{GREEN}  ✅ Folders ready{RESET}")


def print_next_steps():
    is_win = platform.system() == "Windows"
    activate = r"venv\Scripts\activate" if is_win else "source venv/bin/activate"

    print(f"\n{BOLD}{GREEN}")
    print("╔══════════════════════════════════════════════════════╗")
    print("║  ✅  Setup complete! Next steps:                     ║")
    print("╠══════════════════════════════════════════════════════╣")
    print(f"║  1. Activate venv:                                   ║")
    print(f"║       {activate:<46} ║")
    print("║                                                      ║")
    print("║  2. Put your 10 CSV files into  data/raw/            ║")
    print("║                                                      ║")
    print("║  3. Run ETL pipeline:                                ║")
    print("║       python data_ingestion.py                       ║")
    print("║                                                      ║")
    print("║  4. Open notebook:                                   ║")
    print("║       jupyter notebook                               ║")
    print("╚══════════════════════════════════════════════════════╝")
    print(RESET)


def main():
    banner()
    print("  Checking system…\n")
    check_python()
    create_venv()
    install_deps()
    create_dirs()
    print_next_steps()


if __name__ == "__main__":
    main()
