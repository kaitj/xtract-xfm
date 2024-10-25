"""Command-line interface."""

from argparse import SUPPRESS, ArgumentParser, Namespace, RawDescriptionHelpFormatter
from collections.abc import Sequence
from pathlib import Path

from xtract_xfm import __version__


class XtractXfmArgumentParser:
    """XtractXfm command-line argument parser."""

    def __init__(self) -> None:
        self.parser = ArgumentParser(
            prog="xtract_xfm",
            usage="%(prog)s input_file output_file composite_transform [options]",
            add_help=False,
            formatter_class=RawDescriptionHelpFormatter,
            description="""
xtract_xfm is a tool designed to perform transformation of XTRACT data
between different NHP templates via composite warps provided from RheMAP.""",
        )
        self._add_required_args()
        self._add_metadata_args()

    def _add_required_args(self) -> None:
        """Required arguments."""
        self.parser.add_argument(
            "input_file",
            metavar="input_file",
            type=Path,
            help="path to input file to be transformed",
        )
        self.parser.add_argument(
            "output_file",
            metavar="output_file",
            type=Path,
            help="full file path (including name) to save transformed output",
        )
        self.parser.add_argument(
            "composite_transform",
            metavar="transform",
            type=Path,
            help="path to composite transform to be applied",
        )

    def _add_metadata_args(self) -> None:
        """Metadata arguments."""
        self.parser.add_argument(
            "--help",
            action="help",
            default=SUPPRESS,
            help="Show this help message and exit.",
        )
        self.parser.add_argument(
            "--version",
            action="version",
            version=f"{__package__} {__version__}",
            help="show version",
        )

    def parse_args(self, args: Sequence[str] | None = None) -> Namespace:
        """Parse command-line arguments."""
        return self.parser.parse_args(args)
