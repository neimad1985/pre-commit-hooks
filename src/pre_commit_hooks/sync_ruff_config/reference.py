from importlib.resources import files


def read_reference() -> str:
    return files(__package__).joinpath("ruff.toml").read_text()
