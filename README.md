# FairEmail Morphe patches

Unofficial GPL-3.0-licensed Morphe patch source for the official GitHub FairEmail **1.2337a and 1.2338a** APKs (package `eu.faircode.email`).

**[Add patch source to Morphe Manager](https://morphe.software/add-source?github=rikunode/fairemail-morphe-patches)**

## Included patches

| Patch | Default | What it does |
|---|---|---|
| Permanently hide donation banner | On | Hide the support banner above the mail list |
| Enable local settings export (experimental) | Off | Open FairEmail's existing encrypted account/settings export dialog |
| Enable local Pro features (experimental) | Off | Enable application-local Pro feature checks, without modifying purchase records |

The two experimental options must be selected manually.

## Supported original APKs — exact version and SHA-256

| Version | APK (official upstream GitHub release) | SHA-256 |
|---|---|---|
| 1.2337 (v1.2337a) | [FairEmail-v1.2337a-github-release.apk](https://github.com/M66B/FairEmail/releases/download/1.2337/FairEmail-v1.2337a-github-release.apk) | `e8337c82f9829f2c2ad89c04a27af62d74daa3be141558845bd6ee0ddd8c79c8` |
| 1.2338 (v1.2338a) | [FairEmail-v1.2338a-github-release.apk](https://github.com/M66B/FairEmail/releases/download/1.2338/FairEmail-v1.2338a-github-release.apk) | `666b9f4ada53f69199355f1ccc2bed73e01fa23786fc0189cf81cc51932dc5a9` |

These exact **GitHub APKs** have been tested with Morphe Desktop. Other flavors (Google Play, F-Droid, large builds), older versions, and newer versions have **not** been verified.

## IMPORTANT — do not delete your existing FairEmail

**Morphe re-signs the APK. A re-signed APK cannot update an official FairCode-signed installation in place and keep app data on an unrooted phone.** Do not use auto-uninstall-on-conflict, clear storage, uninstall official FairEmail, or assume an existing Gmail login will carry over.

Gmail official OAuth in a Morphe-re-signed FairEmail fails FairEmail's signing certificate restrictions. Personal Google accounts eligible for app passwords can try setting up Gmail as an **Other provider / IMAP** account using their own Google app password. Never share passwords or backup archives.

**Verification boundary (2026-10-28):** [GitHub Actions](https://github.com/rikunode/fairemail-morphe-patches/actions/runs/40550825839) completed successfully. The published v0.2.0 MPP was downloaded back from the public Release, with SHA-256 `cde8e2184b7c567650c374247b80e20f662d5c9b913c63285e97c4b6053bd225`. Morphe Desktop v1.19.1 independently resolved the GitHub repository URL, downloaded the 43,280-byte MPP, and recognized all three patches with the correct compatibility targets. The **public remote MPP** was also applied to the pinned original 1.2337a and 1.2338a APKs, with three patches applied, zero failures and successful APK rebuilds in both cases (these remote-test outputs were unsigned). Earlier local signed APKs and targeted DEX-prefix checks also passed. **Android Morphe Manager import on an actual phone, app launch, Gmail login, encrypted backup creation, and second-device restore remain unverified.** Treat this as a preview for controlled testing, not a guaranteed data migration.

## Use in Morphe Manager

1. Add this repository as a patch source using the link above.
2. Provide an unmodified official GitHub FairEmail 1.2337a or 1.2338a APK.
3. Select patches. The export and Pro options are disabled by default.
4. Only install the resulting APK in an **isolated test environment** with no important app data. Existing stock installation should remain untouched.

This repository ships patch sources and an MPP bundle, **not** a pre-patched FairEmail APK. Preserve the original keystore of any installed Morphe-signed app for later updates.

## Verification and source build

The build uses Java 21 and the Gradle wrapper. CI checks out pinned public Morphe patcher and Gradle plugin commits into the local build-logic directories.

Run `./gradlew :patches:generatePatchesList`, `python scripts/validate_morphe_metadata.py`, `python scripts/validate_morphe_bundle.py`.

Version: **0.2.0 preview**. This independent project is not affiliated with FairEmail, FairCode, or Morphe. Licensed under GPL-3.0. See LICENSE.
