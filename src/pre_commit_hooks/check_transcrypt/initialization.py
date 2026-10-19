import subprocess
from pathlib import Path

CIPHER = "aes-256-cbc"


def is_initialized(repository: Path) -> bool:
    # --name-only n'affiche que le nom de la clé : le mot de passe ne sort jamais.
    completed = subprocess.run(
        ["git", "-C", str(repository), "config", "--local", "--get-regexp", "--name-only", r"^transcrypt\.password$"],
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.returncode == 0


def initialize(repository: Path, password_file: Path) -> None:
    password = password_file.read_text().strip()
    subprocess.run(
        ["transcrypt", "--cipher", CIPHER, "--password", password, "--yes"],
        cwd=repository,
        check=True,
        capture_output=True,
    )


def ensure_initialized(repository: Path, password_file: Path) -> bool:
    """Initialise transcrypt au besoin et indique si l'initialisation vient d'avoir lieu."""
    if is_initialized(repository):
        return False
    initialize(repository, password_file)
    return True
