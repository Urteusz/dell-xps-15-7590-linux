# References

Checked on October 17, 2026. Hardware status in this project is based on the [local validation report](VERIFIED-2026-10-17.md), not solely on published support lists.

- [Dell XPS 15 7590 specifications](https://dl.dell.com/topicspdf/xps-15-7590-laptop_users-guide_en-us.pdf)
- [Linux Wireless: iwlwifi](https://wireless.docs.kernel.org/en/latest/en/users/drivers/iwlwifi.html)
- [NVIDIA kernel module documentation](https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/kernel-modules.html)
- [libfprint supported devices](https://fprint.freedesktop.org/supported-devices.html): development-version coverage, not a guarantee about distribution packages.
- [Goodix53x5 upstream](https://github.com/AndyHazz/goodix53x5-libfprint): the bundled snapshot is pinned to an older local revision; see its provenance file and original credits.
- [SDDM fingerprint timeout issue #1840](https://github.com/sddm/sddm/issues/1840), plus the installed `pam_fprintd(8)` manual.
- [RPM Fusion configuration](https://rpmfusion.org/Configuration), [NVIDIA](https://rpmfusion.org/Howto/NVIDIA), and [Secure Boot](https://rpmfusion.org/Howto/Secure%20Boot). Automated access to the latter guides was blocked during validation; review current instructions before changing driver branches or signing configuration.
- Installed DNF5 `dnf download --help` for dependency resolution and download options.

Local evidence includes sysfs, PCI/USB driver bindings, RPM metadata, NVIDIA API, Intel/PRIME OpenGL, NetworkManager state, PipeWire, Bluetooth, journal timings, and fwupd device discovery. Public reports omit raw device identifiers and biometric data.
