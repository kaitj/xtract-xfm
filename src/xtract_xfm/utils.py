"""Helper utility functions."""

import logging
from argparse import Namespace

import yaml
from styxdefs import (
    LocalRunner,
    Runner,
    set_global_runner,
)
from styxdocker import DockerRunner
from styxsingularity import SingularityRunner


def setup_logger(
    level: int | None = None,
    debug: bool = False,
) -> logging.Logger:
    """Setup logging function."""
    logger = logging.getLogger(__package__)

    if debug:
        level = logging.DEBUG
    else:
        match level:
            case 0:
                level = logging.CRITICAL
            case 1:
                level = logging.ERROR
            case 2:
                level = logging.WARNING
            case _:
                level = logging.INFO

    if not logger.hasHandlers():
        logger.setLevel(level)
        ch = logging.StreamHandler()
        ch.setLevel(level)
        formatter = logging.Formatter("[%(levelname).1s] %(message)s")
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger


def setup_runner(args: Namespace, logger: logging.Logger) -> Runner:
    """Setup styx runner."""
    logger.info("Setting up StyxRunner")
    if args.runner_tmpdir:
        args.runner_tmpdir.mkdir(parents=True, exist_ok=True)

    match args.runner_choice:
        case "docker":
            runner = DockerRunner()
        case "singularity" | "apptainer":
            if args.runner_config is None:
                raise ValueError("Runner config is not provided")
            with open(args.runner_config, "r") as container_config:
                images = yaml.safe_load(container_config)
            runner = SingularityRunner(images=images)
        case _:
            runner = LocalRunner()

    runner.data_dir = args.runner_tmpdir
    set_global_runner(runner)

    return runner
