#!/usr/bin/env python3
"""Promote candidate artifacts only after re-validating the paired evaluation gate."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Iterable, Sequence

try:
    from .paired_eval import PromotionBlocked, require_promote
except ImportError:
    from paired_eval import PromotionBlocked, require_promote


def promote_artifacts(report_path: Path, artifact_pairs: Iterable[tuple[Path, Path]]) -> list[Path]:
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PromotionBlocked(f"Cannot read evaluation report: {exc}") from exc
    require_promote(report)
    pairs = [(Path(src), Path(dst)) for src, dst in artifact_pairs]
    if not pairs:
        raise ValueError("At least one SOURCE=DESTINATION artifact pair is required")

    staged: list[tuple[Path, Path]] = []
    try:
        # Validate and stage every candidate before replacing any champion file.
        for source, destination in pairs:
            if not source.is_file():
                raise FileNotFoundError(f"Candidate artifact does not exist: {source}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            fd, temp_name = tempfile.mkstemp(prefix=f".{destination.name}.", suffix=".staged", dir=destination.parent)
            os.close(fd)
            stage = Path(temp_name)
            shutil.copy2(source, stage)
            staged.append((stage, destination))
        for stage, destination in staged:
            os.replace(stage, destination)
        return [destination for _, destination in staged]
    finally:
        for stage, _ in staged:
            stage.unlink(missing_ok=True)


def _parse_pair(value: str) -> tuple[Path, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("Use SOURCE=DESTINATION")
    source, destination = value.split("=", 1)
    if not source or not destination:
        raise argparse.ArgumentTypeError("Use SOURCE=DESTINATION")
    return Path(source), Path(destination)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=Path("eval/latest_eval.json"))
    parser.add_argument("--artifact", action="append", required=True, type=_parse_pair,
                        help="Candidate source and Champion destination, e.g. candidate.pkl=champion.pkl")
    args = parser.parse_args(argv)
    try:
        destinations = promote_artifacts(args.report, args.artifact)
    except (PromotionBlocked, OSError, ValueError) as exc:
        parser.error(str(exc))
    for destination in destinations:
        print(f"PROMOTED {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
