#!/usr/bin/env python3
"""Preflight the *Android Morphe Manager* remote-source metadata format.

MorpheAsset.createdAt uses kotlinx.datetime.LocalDateTime, not Instant.
Do not accept RFC3339/ISO8601 timezone offsets or a trailing "Z".
"""
import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
REPOSITORY = "rikunode/fairemail-morphe-patches"
PATCH = "Permanently hide donation banner"
VERSION = "0.2.0"


def validate_asset(asset: dict, index: dict) -> None:
    if not isinstance(asset, dict) or not isinstance(index, dict):
        raise ValueError("Bundle and index must be JSON objects")

    timestamp = asset.get("created_at")
    if not isinstance(timestamp, str) or re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", timestamp) is None:
        raise ValueError("Morphe Manager requires offset-free LocalDateTime: YYYY-MM-DDTHH:MM:SS (no Z or +09:00)")
    try:
        datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
    except ValueError as exc:
        raise ValueError("created_at is not a valid calendar timestamp") from exc

    version = asset.get("version")
    if version != VERSION or index.get("version") != VERSION:
        raise ValueError("patches-bundle/index version mismatch")

    download = asset.get("download_url")
    expected = f"https://github.com/{REPOSITORY}/releases/download/v{VERSION}/patches-{VERSION}.mpp"
    if download != expected or urlsplit(download).scheme != "https":
        raise ValueError("download_url does not match actual expected public Release asset")

    if not isinstance(asset.get("description"), str) or not asset["description"].strip():
        raise ValueError("description must be nonempty")
    if asset.get("signature_download_url") not in ("", None):
        raise ValueError("unexpected signature_download_url; verify release signature asset")

    patches = index.get("patches")
    names = {
        "Permanently hide donation banner",
        "Enable local settings export (experimental)",
        "Enable local Pro features (experimental)",
    }
    if not isinstance(patches, list) or len(patches) != 3 or {p.get("name") for p in patches} != names:
        raise ValueError("expected exactly three FairEmail patches")
    for patch in patches:
        packages = patch.get("compatiblePackages")
        if not isinstance(packages, list) or len(packages) != 1:
            raise ValueError("expected exactly one compatible package")
        item = packages[0]
        if item.get("packageName") != "eu.faircode.email":
            raise ValueError("package must be FairEmail")
        targets = item.get("targets")
        if not isinstance(targets, list) or len(targets) != 2:
            raise ValueError("expected two version targets")
        by_version = {}
        for target in targets:
            version = target.get("version")
            codes = target.get("versionCodes")
            if version not in ("1.2337", "1.2338") or version in by_version:
                raise ValueError("FairEmail versionName mismatch")
            if not isinstance(codes, dict) or len(codes) != 4 or set(codes.values()) != {int(version.split(".")[-1])}:
                raise ValueError("FairEmail versionCode pin mismatch")
            by_version[version] = codes
        if set(by_version) != {"1.2337", "1.2338"}:
            raise ValueError("Missing FairEmail version target")
        if patch.get("default") is not (patch["name"] == "Permanently hide donation banner"):
            raise ValueError("Unsafe patch default")


def main() -> None:
    asset = json.loads((ROOT / "patches-bundle.json").read_text(encoding="utf-8"))
    index = json.loads((ROOT / "patches-list.json").read_text(encoding="utf-8"))
    validate_asset(asset, index)
    print("MORPHE_MANAGER_SOURCE_METADATA_PASS: offset-free timestamp, public release URL, three FairEmail patches, two exact app versions")


if __name__ == "__main__":
    main()
