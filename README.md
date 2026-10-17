# Dell XPS 15 7590 Linux Support Kit

Driver setup, hardware diagnostics, and Goodix fingerprint integration for the **Dell XPS 15 7590** running **Fedora 43 KDE (x86_64)**.

Most hardware uses drivers included in Linux. This kit brings together the required packages, NVIDIA setup, offline package downloads, and a snapshot of the experimental Goodix driver.

## Hardware support

Validated on an Intel Core i7-9750H configuration with UHD 630, GTX 1650, and Killer AX1650x / Intel AX200. Last checked: **October 17, 2026**.

| Component | Driver | Validation |
| --- | --- | --- |
| Intel UHD 630 | `i915`, Mesa | Accelerated OpenGL verified |
| NVIDIA GTX 1650 | `nvidia`, RPM Fusion akmods | Driver API and PRIME OpenGL verified |
| Wi-Fi AX200 / AX1650x | `iwlwifi` | Connected successfully |
| Bluetooth | `btusb`, `btintel` | Firmware loaded; controller enabled |
| Audio | `snd_hda_intel`, PipeWire | Playback and capture devices detected |
| Webcam | `uvcvideo` | V4L2 and PipeWire devices detected |
| Touchpad | I2C HID, libinput | Detected; intermittent cursor jumps logged |
| SD reader, NVMe, Thunderbolt | Kernel drivers | Controllers detected and bound |
| Goodix `27c6:5395` | Custom libfprint / SIGFM | Successful match observed; experimental |

Detection does not establish full functional coverage. Cold-boot fingerprint login, suspend/resume, external displays, peripherals, audio playback/capture, and camera streaming still require testing. See the [validation report](docs/VERIFIED-2026-10-17.md) for known issues.

## Quick start

Clone or download this repository, open its directory, and run commands as your normal user. Requirements: Fedora 43 x86_64, Python 3, DNF5, and administrator access for installation.

1. Configure [RPM Fusion](https://rpmfusion.org/Configuration) for NVIDIA packages.
2. Review the package selection and installation command:

   ```bash
   python3 scripts/setup.py plan
   python3 scripts/setup.py install
   ```

3. Install the packages and finish the NVIDIA module build:

   ```bash
   python3 scripts/setup.py install --apply
   sudo akmods --force
   ```

   Follow [installation instructions](docs/INSTALL.md) for Secure Boot and reboot verification. Goodix installation is separate.

4. Check your hardware:

   ```bash
   python3 scripts/diagnose.py --output reports/local.json
   ```

The installer checks the laptop model, Fedora release, and architecture. Commands preview changes unless `--apply` is supplied. Package installation retains DNF's confirmation prompt. Script messages currently include Polish text.

## Fingerprint login

The Goodix sensor requires a custom driver. This repository preserves its source snapshot and integration changes; the package installer does not install it automatically. See [Goodix setup and limitations](docs/FINGERPRINT.md).

For an existing Goodix installation, an optional SDDM fix limits fingerprint verification to one attempt with an eight-second timeout before password fallback:

```bash
python3 scripts/fix-login.py
sudo python3 scripts/fix-login.py --apply
```

The fix backs up the SDDM configuration. It limits waiting time; cold-boot recognition remains unverified.

## Documentation

- [Installation and recovery](docs/INSTALL.md)
- [Offline installation](docs/OFFLINE.md)
- [Fingerprint integration and login troubleshooting](docs/FINGERPRINT.md)
- [Hardware IDs](hardware/7590.md)
- [Validation results](docs/VERIFIED-2026-10-17.md)
- [Functional test checklist](docs/TESTING.md)
- [References](docs/SOURCES.md)

## License

Project scripts and documentation: [MIT](LICENSE). Bundled Goodix/SIGFM sources retain their upstream licensing and attribution; see [third-party notices](THIRD_PARTY.md).
