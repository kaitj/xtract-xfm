"""Entrypoint of application."""

from xtract_xfm.cli import XtractXfmArgumentParser


def main() -> None:
    """xtract_xfm entrypoint."""
    parser = XtractXfmArgumentParser()
    args = parser.parse_args()


if __name__ == "__main__":
    main()
