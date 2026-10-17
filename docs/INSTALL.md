# Installation

Supported target: **Dell XPS 15 7590, Fedora 43, x86_64**. Other distributions and releases need their own package manifest. Run scripts as a normal user; installation invokes `sudo`.

## Package repositories

Enable RPM Fusion using its [configuration guide](https://rpmfusion.org/Configuration). For Fedora 43:

```bash
sudo dnf install https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-43.noarch.rpm https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-43.noarch.rpm
```

Review the [NVIDIA guide](https://rpmfusion.org/Howto/NVIDIA) before changing an existing driver installation.

## Install

```bash
python3 scripts/setup.py plan
python3 scripts/setup.py install
python3 scripts/setup.py install --apply
```

Default profiles: kernel/firmware and desktop hardware support, NVIDIA, and diagnostic tools. For the base system and tools only:

```bash
python3 scripts/setup.py install --profiles base tools --apply
```

The package installer does not configure GRUB, fan control, power-management services, or fingerprint authentication. Avoid adding overlapping power managers without reviewing your existing configuration.

## NVIDIA and Secure Boot

Wait for the module build to finish:

```bash
sudo akmods --force
modinfo -F version nvidia
modinfo -F vermagic nvidia
```

With Secure Boot enabled, follow the [RPM Fusion signing procedure](https://rpmfusion.org/Howto/Secure%20Boot) and `/usr/share/doc/akmods/README.secureboot`. Check the current state with `mokutil --sb-state`. The scripts do not enroll keys or change UEFI settings.

Reboot after changing the kernel or NVIDIA driver, then verify:

```bash
nvidia-smi
__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia glxinfo -B
python3 scripts/diagnose.py --output reports/after-install.json
```

The reference machine used NVIDIA Open Kernel Module 580.178.04. Downloaded packages may be newer; this is a recorded working version, not a version pin.

## Recovery

Keep the previous working kernel available in the boot menu until the new one is verified. Use `dnf history list` and `dnf history info <ID>` to inspect package changes before considering a rollback.

The optional fingerprint login fix changes `/etc/pam.d/sddm` and prints a backup path and restore command. See [fingerprint troubleshooting](FINGERPRINT.md). Do not restart SDDM inside an active desktop session.
