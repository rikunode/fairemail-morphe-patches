# FairEmail Morphe release-readiness audit

Audit date: 2026-10-29 JST. Target: **the independent Morphe patch bundle**, not an upstream FairEmail release or a pre-patched APK.

## Product requirements traced from the original design

- Unrooted Android devices; no per-user Google Cloud setup.
- Preserve Gmail OAuth login when FairEmail's official GitHub APK is re-signed.
- Preserve access to an existing official app installation; do **not** uninstall or clear its data.
- Integrate upstream Morphe Clone app behavior into the **same patch source**, enabled by default, retaining the existing `.morphe` package suffix while explicitly disabling the separate Morphe Clone app selection.
- Hide the in-app support banner permanently.
- Expose FairEmail local Pro functionality without falsely representing purchase or changing app store transactions.
- Export encrypted account/settings backups, transfer them to another device, and import successfully.
- Suppress intrusive changelog popups while preserving the manually viewable changelog.
- Make the patch bundle obtainable and updateable from Morphe Manager with a GitHub source, reproducible builds and exact APK version pins.
- Publish reproducible, reviewable, clearly unofficial GPLv3 source; do not distribute personal credentials or private keystores.

## Evidence and precise verification boundaries

| Feature | Status | Evidence / limitation |
|---|---|---|
| Source distribution via Morphe Android | VERIFIED | User screenshot of four patches recognized; dev .2 remote metadata verified for five patches |
| Kotlin compile and Android .mpp build (five patches) | VERIFIED | GitHub Actions run 40821254754 completed successfully |
| Integrated clone (sixth patch, compiled/installed) | PENDING | Source transplanted with GPLv3 notices and default `.morphe` suffix; device package/signer identity and provider authority compatibility still require regression tests |
| Google consent and Gmail account-added dialog on modified build | VERIFIED UI | User-supplied Android screenshots, 2026-10-29 |
| Reading a newly received Gmail email from another account | VERIFIED UI | User-supplied FairEmail screenshot plus Gmail connector send and inbox read-back, 2026-10-29 |
| Password-backed settings export produced a nonempty file | VERIFIED FILE | User attached a 14,336-byte .backup; binary header/entropy and length match encrypted backup format, no decryption attempted |
| Account settings imported on another device | USER-REPORTED SUCCESS | User explicitly confirmed import success; the resulting Gmail sync after import has not been verified |
| FairEmail SMTP transmission to another mailbox | NOT YET VERIFIED | Gmail connector sending **to** FairEmail is not a test of outgoing SMTP **from** the modified APK |
| Imported Gmail OAuth refresh after token expiry / app restart | NOT YET VERIFIED | Must test without manually logging in again |
| Upgrade a clone in place with retained data and identical signing key | NOT YET VERIFIED | Preserve signing certificate and package identity; no uninstall/reinstall |
| Changelog popup hidden on first eligible startup | NOT YET VERIFIED | Compiled and published patch only; user has not confirmed on-device behavior for dev .2 |
| Entire local Pro feature suite | NOT YET VERIFIED | Both Pro and export-only patches were previously selected; export success cannot isolate the global Pro check |
| Other Gmail / Outlook OAuth providers or Android variants | NOT YET VERIFIED | Tested path is Gmail on the supplied build |
| Exact five-patch application to pristine pinned APK, unsigned rebuilt APK integrity | NOT YET VERIFIED BY CI | Build and DEX-index validation do not execute a full patch application |

## P0 release gates — must pass before changing the default stable source

1. Confirm the **imported** account on the destination Android device receives a **new** message, not only folders that came from the backup.
2. Send a message **from the patched FairEmail** and confirm delivery to a different mailbox (SMTP).
3. Test refresh after the existing access token expires (typically ~1 hour or greater), app restart, and another delayed sync; verify no reauthorization required. Repeat on the destination device.
4. Test updating the installed clone with the **same signing certificate** and **same package name**, without uninstalling/clearing data, while retaining accounts and the new token. Do not copy private signing keys into the repository.
5. Confirm the published six-patch development bundle suppresses the *automatic* changelog dialog after the appropriate first-run/version transition; confirm the manual changelog is still available.
6. Run end-to-end application test on the exact upstream 1.2338a GitHub APK (SHA-256 `666b9f4ada53f69199355f1ccc2bed73e01fa23786fc0189cf81cc51932dc5a9`), applying the six integrated patches **without** Morphe's separate Clone app. Compare built-in vs older external Clone app results (manifest package, permissions, provider authorities), then install/update with the **same signing key** and check the accounts remain available.
7. Capture the release permissions provenance privately (user reports upstream developer and Google consent for the intended OAuth use). Do not publish private correspondence or claim that a client ID alone demonstrates permission.

## P1 tests and hardening

- Verify optional features independently: export-only with global Pro **off**; global Pro on with export-only **off**; changing these options must not alter purchase records.
- Verify Gmail account setup with and without Clone app to distinguish the OAuth callback receiver; confirm the actual installed package identity.
- Verify failure modes: wrong backup password, damaged backup, duplicate import/account, missing credentials, corrupted/unsupported APK, missing network, and account revoked externally.
- Test fair use on 1.2337a: only the three compatible patches should appear; OAuth/changelog should be 1.2338-only.
- Check Android supported versions and ARM64/ARM32 compatibility, package and keystore migrations, and the first-launch welcome experience.
- Confirm notification/sync service behavior after reboot and with battery restrictions.
- Confirm final release notes/README match present evidence, not historical v0.2.0 test status.

## Backup security and privacy

FairEmail 1.2338 exports a JSON object including account and identity records, rules, folders, preferences, and potentially live OAuth refresh state in the account/identity `password` fields. **An exported file is credential-bearing sensitive data.**

- A **nonempty passphrase is mandatory**; the original code writes plain JSON when the password is empty.
- In 1.2338, the password-encrypted v0 format uses PBKDF2-HMAC-SHA1 (65,536 iterations), a random salt and IV, and AES-256-CBC. This provides confidentiality given a strong password but is **not authenticated encryption**; corruption/tampering is not reliably detected cryptographically.
- Use a unique strong passphrase, keep two separate private copies of the encrypted backup, and test restoration before deleting any original data.
- Never upload the user's backup, OAuth tokens, private signing keystore, or account-specific logs to public GitHub Releases, CI artifacts or README examples.
- The backup is primarily settings/account data, not a complete offline mailbox archive.

## Release artifact and channel design

- **main**: stable `v0.2.0` remains unchanged while gates are open.
- **dev**: currently published `v0.2.1-dev.2`, five patches, `patches-bundle.json` and `patches-list.json` agree. Proposed next preview `v0.2.1-dev.3` includes **sixth integrated clone** and is not yet production-verified.
- **release/readiness-0.3.0**: documentation and tests for the next stable candidate, NOT an announcement of a completed release.
- Candidate target name: `v0.3.0-rc.1`. Produce a *draft* or isolated candidate first; do not silently replace stable `main`.
- Ship the **.mpp patch bundle and source**, not a pre-signed FairEmail APK or user-specific backup.
- Provide the exact original APK link/hash, compiled bundle SHA-256, Git commit SHA, compatibility matrix, known issues, update/rollback procedure and changelog.
- Preserve version pinning; avoid rewriting a published tag or release asset. Test Morphe Android index loading, not only JVM/Gradle compilation.
- Confirm API use is covered by permissions before advertising widespread public Gmail OAuth compatibility; the user's stated permission is not independently verifiable from repository contents.

## Go / no-go

**Current status: RELEASE CANDIDATE PREPARATION; NOT STABLE-READY.** Account import is user-confirmed, but imported sync, outbound SMTP, token refresh, clone update signing, changelog suppression on-device and six-patch APK application and integrated clone compatibility still require evidence. Do not convert these to PASS based on static tests or a successful MPP build.
