# Goodix fingerprint reader

Sensor: **Goodix HTK32, USB `27c6:5395`**. Support uses an experimental custom libfprint driver with SIGFM matching. This ID was absent from the upstream libfprint supported-device list when checked on October 17, 2026.

## Source snapshot

`vendor/goodix53x5/` preserves the reference machine's driver sources and local modifications. See `provenance.json` for upstream URLs and exact commits.

- `local-driver.patch` records changes already included in the copied sources. Do not apply it again.
- `libfprint-integration.patch` integrates the driver and SIGFM into the pinned libfprint source tree.
- Original source headers, README, and license notices are retained.

Prepare the source tree from the repository root:

```bash
git clone https://gitlab.freedesktop.org/libfprint/libfprint.git build/libfprint
git -C build/libfprint checkout ee422fc3c5feae6e3bc290a23f0c625dcb934189
git -C build/libfprint apply ../../vendor/goodix53x5/libfprint-integration.patch
cp -r vendor/goodix53x5/drivers/goodix53x5 build/libfprint/libfprint/drivers/
cp -r vendor/goodix53x5/sigfm build/libfprint/libfprint/
```

Build requirements include Meson, Ninja, C/C++ compilers, GLib, libgusb, OpenSSL, OpenCV development packages, and dependencies of the selected libfprint drivers. Follow the bundled [upstream README](../vendor/goodix53x5/README.md) for build integration. The snapshot is not a tested, distribution-ready RPM and is not installed by `setup.py`.

The reference installation loads its custom library from `/usr/local/lib64` through an `fprintd` service override. A bundled udev rule prevents `cdc_acm` from claiming the sensor. Review both against your distribution before installation. Newer upstream Goodix revisions may differ from this preserved snapshot.

## SDDM password delay

A standalone `pam_fprintd.so` rule before `password-auth` causes SDDM to wait for fingerprint verification before checking a password. The default timeout is 30 seconds. This PAM stack processes authentication sequentially; KDE screen unlocking uses a separate fingerprint stack.

On the reference machine, four recorded boots showed 30-second timeouts, including two attempts during one boot. Sensor initialization took less than a second. A later verification matched successfully. The reported three-to-four-minute continuous password delay was not established by these logs.

For the expected existing SDDM configuration, preview and apply the bounded-wait fix:

```bash
python3 scripts/fix-login.py
sudo python3 scripts/fix-login.py --apply
```

This sets `timeout=8 max-tries=1`, preserves password fallback, and prints the backup path and restore command. It changes only the standalone SDDM fingerprint rule and refuses unexpected configurations. The limit applies to the verification stage, not the complete login process. It does not resolve the underlying cold-boot recognition issue.

For password-only SDDM login while retaining the separate KDE fingerprint stack:

```bash
sudo python3 scripts/fix-login.py --mode password --apply
```

Choose one mode. The password-only change removes the rule, so running the fixer again requires restoring the original configuration first. Test on the next normal login; restarting SDDM would end the current session.

## Verify recognition

1. After a cold boot, keep your finger off the power button until the login screen is ready. Start a login attempt, then touch the enrolled finger to the sensor.
2. After login, inspect timings:

   ```bash
   python3 scripts/login-timeline.py
   python3 scripts/login-timeline.py --boot -1
   ```

3. Run `fprintd-verify` and check that the enrolled finger matches and an unenrolled finger is rejected.
4. Compare cold boot, restart, and screen unlock. Do not publish biometric images or templates.

Cold-boot recognition after the timeout change has not been verified. The reference system also logged SELinux denials involving `nr_hugepages`; a later match succeeded despite these denials. Review AVC records and library labels before changing policy. Do not disable SELinux or change biometric thresholds as an unvalidated workaround.
