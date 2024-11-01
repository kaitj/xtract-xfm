"""Entrypoint of application."""

import shutil
import sys
from collections.abc import Sequence

from niwrap import ants

from xtract_xfm import io, utils
from xtract_xfm.cli import XtractXfmArgumentParser


def main(args: Sequence[str] | None = None) -> None:
    """xtract_xfm entrypoint."""
    parser = XtractXfmArgumentParser()
    if args is None:
        args: list[str] = sys.argv[1:]
    args = parser.parse_args(args)

    logger = utils.setup_logger(level=args.verbose, debug=args.debug)

    # Verify necessary input files exist
    io.verify_inputs(
        inputs=[args.input_file, args.template_file, args.transform_file],
        logger=logger,
    )

    runner = utils.setup_runner(args=args, logger=logger)

    # Apply transformation
    logger.info(f"Applying transformation to {args.input_file}")
    xfm = ants.ants_apply_transforms(
        input_image=args.input_file,
        reference_image=args.template_file,
        output=ants.AntsApplyTransformsWarpedOutput(str(args.output_file.name)),
        transform=[ants.AntsApplyTransformsTransformFileName(str(args.transform_file))],
        interpolation=ants.AntsApplyTransformsNearestNeighbor(),
    )
    args.output_file.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(xfm.output.output_image_outfile, args.output_file)

    # Clean up
    if not args.debug:
        logger.info("Cleaning up temporary files")
        shutil.rmtree(runner.data_dir)


if __name__ == "__main__":
    main()
