#!/usr/bin/env python3
"""Read-only checks. Reports intentionally exclude raw logs and device identifiers."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess


def run(argv, env=None):
    if not shutil.which(argv[0]):
        return None, ''
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=25,
                           env={**os.environ, 'LC_ALL': 'C', **(env or {})})
        return p.returncode, p.stdout + p.stderr
    except (OSError, subprocess.TimeoutExpired):
        return None, ''


def read(path):
    try:
        return Path(path).read_text().strip()
    except OSError:
        return ''


def pci_devices():
    devices = {}
    for dev in Path('/sys/bus/pci/devices').glob('*'):
        key = read(dev / 'vendor').removeprefix('0x') + ':' + read(dev / 'device').removeprefix('0x')
        driver = dev / 'driver'
        devices.setdefault(key, []).append(driver.resolve().name if driver.exists() else '')
    return devices


def diagnose():
    checks = []
    def add(name, status, detail):
        checks.append(dict(name=name, status=status, detail=detail))
    devices = pci_devices()
    expected = [('Intel GPU', '8086:3e9b', 'i915'), ('NVIDIA GPU', '10de:1f91', 'nvidia'),
                ('Wi-Fi AX200', '8086:2723', 'iwlwifi'), ('Audio', '8086:a348', 'snd_hda_intel'),
                ('SD reader', '10ec:525a', 'rtsx_pci'), ('Thunderbolt', '8086:15d9', 'thunderbolt'),
                ('NVMe', '144d:a808', 'nvme')]
    for name, ident, driver in expected:
        bound = devices.get(ident)
        add(name, 'PASS' if bound and driver in bound else 'WARN' if bound else 'SKIP',
            f'{ident}: ' + (', '.join(bound) if bound else 'wariant sprzętu nieobecny'))
    rc, output = run(['glxinfo', '-B'])
    add('Intel OpenGL', 'PASS' if rc == 0 and 'Intel' in output and 'Accelerated: yes' in output else 'UNKNOWN',
        'Akceleracja potwierdzona' if rc == 0 and 'Intel' in output and 'Accelerated: yes' in output else 'Brak potwierdzenia; sprawdź sesję graficzną/uprawnienia')
    rc, _ = run(['nvidia-smi', '--query-gpu=name,driver_version', '--format=csv,noheader'])
    add('NVIDIA API', 'PASS' if rc == 0 else 'UNKNOWN',
        'Komunikacja ze sterownikiem' if rc == 0 else 'Brak potwierdzenia; możliwa piaskownica, brak narzędzia lub problem sterownika')
    rc, output = run(['glxinfo', '-B'], {'__NV_PRIME_RENDER_OFFLOAD': '1', '__GLX_VENDOR_LIBRARY_NAME': 'nvidia'})
    add('NVIDIA PRIME', 'PASS' if rc == 0 and 'OpenGL vendor string: NVIDIA' in output else 'UNKNOWN',
        'Test kontekstu OpenGL; bez testu obciążenia')
    rc, output = run(['nmcli', '-t', '-f', 'TYPE,STATE', 'device'])
    add('Wi-Fi connection', 'PASS' if rc == 0 and 'wifi:connected' in output else 'UNKNOWN',
        'Stan połączenia; bez testu przepustowości')
    rc, output = run(['wpctl', 'status'])
    add('PipeWire', 'PASS' if rc == 0 and '[alsa]' in output else 'UNKNOWN',
        'Wykrycie karty; odsłuch i mikrofon wymagają testu ręcznego')
    add('Camera node', 'PASS' if list(Path('/sys/class/video4linux').glob('video*')) else 'UNKNOWN',
        'Rejestracja urządzenia; obrazu nie rejestrowano')
    add('Touchpad', 'PASS' if '06CB:7A13 Touchpad' in read('/proc/bus/input/devices') else 'UNKNOWN',
        'Obecność urządzenia; płynność gestów wymaga testu ręcznego')
    add('Bluetooth controller', 'PASS' if list(Path('/sys/class/bluetooth').glob('hci*')) else 'UNKNOWN',
        'Obecność kontrolera; parowanie nieprzetestowane')
    rc, output = run(['journalctl', '-b', '-k', '--no-pager', '-o', 'cat'])
    markers = [('NVIDIA log', 'NV_ERR_NO_MEMORY'), ('Intel display log', 'Failed to probe lspcon'),
               ('SD filesystem log', 'Filesystem has been set read-only')]
    for name, marker in markers:
        add(name, 'WARN' if marker in output else 'UNKNOWN' if rc != 0 else 'PASS',
            'Znaleziono: ' + marker if marker in output else 'Brak znacznika w dostępnych logach; nie oznacza pełnego testu')
    add('Fingerprint Goodix 5395', 'MANUAL', 'Eksperymentalny sterownik: docs/FINGERPRINT.md; brak testu biometrycznego')
    add('Suspend / HDMI / USB-C / SD read-write', 'MANUAL', 'Wykonaj docs/TESTING.md')
    return dict(date=datetime.now(timezone.utc).isoformat(), model=read('/sys/class/dmi/id/product_name'),
                kernel=platform.release(), checks=checks)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Zapisz raport JSON, np. reports/local.json')
    args = parser.parse_args()
    data = diagnose()
    print(f"{data['model']} | {data['kernel']}")
    for row in data['checks']:
        print(f"{row['status']:7} {row['name']}: {row['detail']}")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print('PASS dotyczy opisanego testu, nie pełnej sprawności podzespołu.')
    return 1 if any(c['status'] == 'WARN' for c in data['checks']) else 0


if __name__ == '__main__':
    raise SystemExit(main())
