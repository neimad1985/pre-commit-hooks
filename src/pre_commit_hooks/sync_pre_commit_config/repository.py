import subprocess
import tempfile
from pathlib import Path


def run_git(*arguments: str) -> str:
    return subprocess.run(["git", *arguments], check=True, capture_output=True, text=True).stdout


def find_latest_tag(repository_url: str) -> str:
    references = run_git("ls-remote", "--tags", "--refs", "--sort=-v:refname", repository_url).splitlines()
    if not references:
        message = f"No tag found in {repository_url}"
        raise LookupError(message)
    _, latest_reference = references[0].split("\t")
    return latest_reference.removeprefix("refs/tags/")


def read_file_at_tag(repository_url: str, tag: str, file_path: str) -> str:
    with tempfile.TemporaryDirectory() as clone_directory:
        run_git("clone", "--quiet", "--depth", "1", "--branch", tag, repository_url, clone_directory)
        return (Path(clone_directory) / file_path).read_text()
