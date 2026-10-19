import subprocess
from pathlib import Path

CIPHER = "aes-256-cbc"


def is_initialized(repository: Path) -> bool:
    # --name-only n'affiche que le nom de la clé : le mot de passe ne sort jamais.
    completed = subprocess.run(
        ["git", "-C", str(repository), "config", "--local", "--get-regexp", "--name-only", r"^transcrypt\.password$"],
        capture_output=True,
        text=True,
    )
    return completed.returncode == 0


def initialize(password_file: Path) -> None:
    password = password_file.read_text().strip()
    subprocess.run(["transcrypt", "--cipher", CIPHER, "--password", password, "--yes"], check=True, capture_output=True)
