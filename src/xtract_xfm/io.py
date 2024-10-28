"""IO related functions."""

from logging import Logger
from pathlib import Path


def verify_inputs(inputs: list[Path], logger: Logger) -> None:
    """Assert all inputs (except output file) exists."""
    for input_ in inputs:
        if input_.is_dir():
            raise IsADirectoryError(f"{input_} is a directory")
        if not input_.exists():
            raise FileNotFoundError(f"{input_} does not exist")
