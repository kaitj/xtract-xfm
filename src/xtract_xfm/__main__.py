"""Entrypoint of application."""

from xtract_xfm.cli import XtractXfmArgumentParser
from xtract_xfm.utils import setup_logger


def main() -> None:
    """xtract_xfm entrypoint."""
    parser = XtractXfmArgumentParser()
    args = parser.parse_args()

    logger = setup_logger(level=args.verbose, debug=args.debug)


if __name__ == "__main__":
    main()
