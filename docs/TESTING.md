# Functional validation

Run diagnostics in a normal terminal inside your desktop session:

```bash
python3 scripts/diagnose.py --output reports/local.json
```

The script reads device and service state. It does not record audio/video, authenticate fingerprints, suspend the computer, or modify configuration.

| Status | Meaning |
| --- | --- |
| `PASS` | The specific reported check passed; not a full component certification. |
| `WARN` | A driver discrepancy or selected error marker was found. |
| `UNKNOWN` | Evidence unavailable, for example missing tools or restricted access. |
| `SKIP` | The expected hardware variant was absent. |
| `MANUAL` | Functional testing is required. |

Exit code 1 indicates warnings. Exit code 0 does not establish complete hardware support.

## Checklist

| Function | Check |
| --- | --- |
| Audio | Test both speaker channels, headphones, input switching, and a microphone recording. |
| Camera | Open a live preview and confirm permissions and stable streaming. |
| Bluetooth | Pair a known device and verify reconnection and sustained use. |
| Touchpad | Test movement, taps, scrolling, and gestures; inspect libinput/KWin logs for jumps. |
| Brightness / Fn | Check brightness range and all relevant hotkeys. |
| Suspend | Save work, suspend and resume; retest Wi-Fi, sound, and both GPUs. Record `/sys/power/mem_sleep`. |
| External displays | Verify resolution, audio, unplug/replug, HDMI and USB-C separately. |
| Thunderbolt | Connect and authorize a known dock, then test its display, USB, and network functions. |
| SD / USB storage | Use healthy test media without important data; verify read/write and safe removal. |
| NVIDIA | Run the PRIME check followed by a known 3D workload; look for new Xid or memory errors. |
| Battery | Observe charging, discharge reporting, and runtime under normal use. |
| Fingerprint | Test enrolled and unenrolled fingers after cold boot, restart, and screen unlock. |

Hibernation also depends on swap and resume configuration. Do not apply unrelated kernel parameters or tuning changes without reproducing a specific issue.

## Script checks

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q scripts
```

These check the package workflow, bundle integrity handling, and guarded PAM edits. They do not replace hardware tests.
