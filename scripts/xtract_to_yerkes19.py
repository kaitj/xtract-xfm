#!/usr/bin/env python
"""Script to transform XTRACT data to Yerkes19 space."""

import os
import shutil
from pathlib import Path

from xtract_xfm.run import main

DATA_DIR = Path("/path/to/data")
RESOURCES_DIR = Path("/path/to/warps")
TMP_DIR = Path(os.environ.get("LOCAL", "/tmp")) / "styx_tmp"
CFG_PATH = Path("/path/to/container/cfg/containers.yaml")

# Extract data
for archive in [*DATA_DIR.glob("*.zip"), *RESOURCES_DIR.glob("**/*.zip")]:
    shutil.unpack_archive(archive, TMP_DIR.parent)

# Transform each macaque ROI from F99 to Yerkes19
xfm_fpath = TMP_DIR.parent / "F99" / "F99_to_YRK_CompositeWarp.nii.gz"
assert xfm_fpath.exists()
ref_nii = (
    TMP_DIR.parent / "tpl-Yerkes19" / "MacaqueYerkes19_v1.2_AverageT1w_restore.nii.gz"
)
assert ref_nii.exists()

xtract_orig = TMP_DIR.parent / "tpl-xtract" / "space-orig" / "Macaque"
for xtract_roi_orig in xtract_orig.glob("*/**/*.nii.gz"):
    tract = xtract_roi_orig.parent.relative_to(xtract_orig)
    xtract_roi_yerkes = (
        TMP_DIR.parent
        / "tpl-xtract"
        / "space-Yerkes19"
        / "Macaque"
        / tract
        / xtract_roi_orig.name
    )
    xtract_roi_yerkes.parent.mkdir(parents=True, exist_ok=True)

    main(
        [
            str(xtract_roi_orig),
            str(ref_nii),
            str(xtract_roi_yerkes),
            str(xfm_fpath),
            "--runner",
            "singularity",
            "--tmpdir",
            str(TMP_DIR),
            "--config",
            str(CFG_PATH),
            "--verbose",
        ]
    )

# Archive transformed files
shutil.make_archive(
    str(DATA_DIR / "tpl-xtract"),
    format="zip",
    root_dir=TMP_DIR.parent,
    base_dir="tpl-xtract",
)
