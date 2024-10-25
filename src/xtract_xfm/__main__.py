"""Entrypoint of application."""

from xtract_xfm import utils
from xtract_xfm.cli import XtractXfmArgumentParser


def main() -> None:
    """xtract_xfm entrypoint."""
    parser = XtractXfmArgumentParser()
    args = parser.parse_args()

    logger = utils.setup_logger(level=args.verbose, debug=args.debug)
    runner = utils.setup_runner(args=args, logger=logger)


if __name__ == "__main__":
    main()
