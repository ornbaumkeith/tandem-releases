# Tandem 0.5.14 — Windows and Android testing

Your goals. Our journey.

Download from **https://ornbaumkeith.github.io/projects/tandem/index.html** or this repository's `tandem-v0.5.14` prerelease. These are actual standalone testing packages, not source-only ZIPs. No Node, npm, Expo Go, app-store account, or local API is needed to use them.

## Packages

- **Windows x64:** `Tandem_0.5.14_Windows_x64_Setup.exe` (120,964,212 bytes).
- **Android:** `Tandem_0.5.14_Android.apk`. Its exact minimum Android version, supported ABIs, package metadata and signing-certificate fingerprint are in the attached `android-package.txt` and `android-signature.txt`.
- Each installer has a matching `.sha256` file. `SHA256SUMS.txt` covers all other release assets.
- Windows is **not Authenticode-signed**. Android uses a dedicated private release-signing identity, not the default debug key. A checksum detects corruption; it does not independently prove publisher identity.

## Windows: verify and install

Download the EXE and its matching `.sha256` into Downloads. If your browser adds a suffix such as `(1)`, select the correct files and update the paths below rather than renaming an older release.

Run this entire block in PowerShell:

```powershell
$ErrorActionPreference = "Stop"
$TandemDownloads = Join-Path $env:USERPROFILE "Downloads"
Set-Location -LiteralPath $TandemDownloads
$TandemInstaller = Join-Path $TandemDownloads "Tandem_0.5.14_Windows_x64_Setup.exe"
$TandemSidecar = "$TandemInstaller.sha256"
if (-not (Test-Path -LiteralPath $TandemInstaller)) { throw "Download the Tandem 0.5.14 Windows installer." }
if (-not (Test-Path -LiteralPath $TandemSidecar)) { throw "Download its matching SHA-256 file." }
$TandemExpected = ((Get-Content -LiteralPath $TandemSidecar -Raw).Trim() -split '\s+')[0]
if ($TandemExpected -notmatch '^[a-fA-F0-9]{64}$') { throw "Invalid checksum file." }
$TandemActual = (Get-FileHash -LiteralPath $TandemInstaller -Algorithm SHA256).Hash
if ($TandemActual -ine $TandemExpected) { throw "Checksum mismatch. Stop and download matching files." }
Write-Host "Checksum matches Tandem 0.5.14."
& ".\Tandem_0.5.14_Windows_x64_Setup.exe"
```

Alternatively, after the same verification: `Start-Process -FilePath $TandemInstaller -Wait`.

Follow setup, then open Tandem from the Start menu or desktop shortcut. This is an unsigned pilot installer: Windows may display an unknown publisher or SmartScreen warning. Continue only if you trust the download; do not disable system-wide security or bypass organizational policy. Keep your previous app/data and any available export before testing. This desktop package uses a different storage origin from a prior localhost development browser; old local-workspace data is not automatically imported.

## Android: install the APK

1. Download the APK from the project page on your Android device.
2. Open it from Downloads. Android may ask you to allow this browser/file manager to install apps. Grant that source permission only if you trust the package, then turn it off after installation.
3. Follow the system prompt and open Tandem. Managed devices may prohibit sideloading. Do not disable device-wide security controls.
4. For future updates, use Tandem APKs signed with the same identity. Keep your data/export before updating; uninstalling may remove local data.

To check the Android download from a Windows computer before transfer, download the APK and matching checksum into Downloads and run:

```powershell
$ErrorActionPreference = "Stop"
Set-Location -LiteralPath (Join-Path $env:USERPROFILE "Downloads")
$TandemApk = ".\Tandem_0.5.14_Android.apk"
$TandemExpected = ((Get-Content -LiteralPath "$TandemApk.sha256" -Raw).Trim() -split '\s+')[0]
if ($TandemExpected -notmatch '^[a-fA-F0-9]{64}$') { throw "Invalid checksum file." }
if ((Get-FileHash -LiteralPath $TandemApk -Algorithm SHA256).Hash -ine $TandemExpected) { throw "Checksum mismatch." }
Write-Host "Android APK checksum matches."
```

## First launch and pairing

Both packages include the public API address: **https://tandem-api-ornbaumkeith.onrender.com**. It is an API, not a web-client download. Register a disposable test account and sign in. If the free service is waking, wait and retry.

Use separate accounts on each device. In Profile's team/connection access, create an invitation and join from your partner's account. Core teams support up to three members. Connected circles are separate teams with read/copy/encourage privileges. Use only the controls for your intended team; never share passwords or private invitation codes publicly.

Local-workspace exploration is separate from cloud accounts. Earlier local databases and browser data are not automatically uploaded or migrated.

## What changed

0.5.14 packages the existing responsive interface as a Windows Electron desktop app and standalone signed Android release APK. The public service address is built into both. The hosted API remains compatible version **0.5.13**, on Render Free with persistent Supabase Free PostgreSQL. No goal rules, scoring, logo, or interface redesign is introduced by this packaging release.

The app retains personal/shared SMART goals, four editable planning steps, dated/recurring actions, calendars and .ics export, working notes, monthly reflections, Daily/Weekly/Monthly/Annual progress, XP/levels, team synchronization, connected circles, section-level privacy, encouragement, avatars and light/dark appearance.

## Test checklist

- Register/sign in; invite a partner; confirm the same shared goal and edits appear on both devices.
- Create a goal and check its four suggested steps. Edit/remove/restore eligible steps and adjust dates.
- Check and reopen an action/step; XP must be reversible rather than duplicated. Completing all planning steps completes the goal.
- Check calendar dates/events and .ics export. Calendar copies are snapshots, not automatic synchronization.
- Save working notes and a monthly reflection; close/reopen and check persistence.
- Connect a separate circle. Hide steps/actions/reflections and confirm they are absent from that circle. Working notes remain private.
- Test light/dark appearance, keyboard/text sizing, phone/tablet layouts and rotation.
- On Android, explicitly apply a device reminder and test permission denial and scheduling. Saving preferences alone does not schedule notifications.
- Reopen the app, test network interruption/reconnection, and confirm no duplicate XP or lost edits.

## Validation and limitations

- The actual Windows NSIS installer completed a silent installation into a path containing spaces in a Windows GitHub runner. The installed app launched with the correct title/version, `app://tandem` origin, and no renderer Node access. Personal-PC and interactive wizard acceptance remain open.
- Android build, release signature/package/permission checks and emulator launch must pass before publication. The attached evidence records the actual result.
- Fresh Node 24 source checks: locked installations, TypeScript and release consistency passed; **65 tests passed, 0 failed, 1 skipped**. The skipped PostgreSQL integration fixture was not configured in this run. Earlier live hosted account/privacy/redeploy acceptance is separate evidence.
- October 27 dependency audits: app/Expo tooling **4 high** findings; server **0**; desktop **0**. Findings include node-forge and an Expo CLI nested Zod dependency, with affected parent packages counted too. They are not cleared by passing tests; no forced incompatible framework downgrade was applied.
- Physical Windows/Android phones/tablets, the full supported-OS matrix, hardware notification/calendar permission behavior and hardware offline replay remain open. Apple releases are deferred.
- Android's local reminders require OS permission. Windows has in-app check-ins and .ics export, not native mobile notifications. Partner activity is synchronized in-app; remote push delivery is not provided.
- **Password-recovery email is unavailable.** Use a password manager and disposable test credentials. Reset requests fail safely without exposing tokens.
- Render Free can sleep; Supabase Free can pause or hit quotas. Service availability is conditional on free-tier limits. Off-service encrypted backup/restore remains unvalidated. Avoid sensitive or irreplaceable data during this pilot.
- Windows session credentials follow the web session-storage model. Android uses SecureStore. No whole-workspace encryption or independent security certification is claimed.

Application source, signing keys/passwords, user databases and provider secrets are excluded from this public repository and its release assets. Android platform tooling has its own licenses; free tooling is not automatically open source.
