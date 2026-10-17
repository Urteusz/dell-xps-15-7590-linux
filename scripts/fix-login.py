#!/usr/bin/env python3
"""Bound fingerprint wait in SDDM; preserve password stack and existing authselect files."""
import argparse
from datetime import datetime, timezone
import difflib
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


def patched(text, mode='timeout'):
    lines = text.splitlines(keepends=True)
    found = 0
    result = []
    for line in lines:
        if re.match(r'^\s*auth\s+sufficient\s+pam_fprintd\.so(?:\s|$)', line):
            found += 1
            if mode == 'password':
                result.append('# Fingerprint omitted only for SDDM; see Linux kit backup.\n')
            else:
                result.append('auth        sufficient    pam_fprintd.so timeout=8 max-tries=1\n')
        else:
            result.append(line)
    if found != 1:
        raise ValueError('Oczekiwano dokładnie jednej samodzielnej reguły sufficient pam_fprintd w SDDM.')
    if not any(re.match(r'^\s*auth\s+substack\s+password-auth\s*$', line) for line in result):
        raise ValueError('Brak oczekiwanego stosu hasła password-auth; przerwano.')
    return ''.join(result)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--apply', action='store_true')
    p.add_argument('--mode', choices=['timeout', 'password'], default='timeout',
                   help='timeout: do 8 s na palec; password: SDDM wyłącznie z hasłem')
    args = p.parse_args()
    target = Path('/etc/pam.d/sddm')
    old = target.read_text()
    new = patched(old, args.mode)
    print(''.join(difflib.unified_diff(old.splitlines(True), new.splitlines(True),
                                       fromfile='sddm (before)', tofile='sddm (after)')))
    if old == new or not args.apply:
        return
    if os.geteuid() != 0:
        sys.exit('Zapis wymaga administratora: sudo python3 scripts/fix-login.py --apply')
    # Abort rather than overwrite a concurrent modification or a managed symlink.
    if target.is_symlink() or target.read_text() != old:
        sys.exit('Plik zmienił się lub jest symlinkiem; przerwano.')
    if 'pam_fprintd.so' in Path('/etc/pam.d/password-auth').read_text():
        sys.exit('password-auth też zawiera czytnik; wymaga osobnego przeglądu.')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    backup_dir = Path('/var/backups/xps7590-login')
    backup_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    backup = backup_dir / ('sddm.' + stamp)
    shutil.copy2(target, backup)
    # Keep original inode, ownership, permissions and SELinux label.
    with target.open('r+') as stream:
        stream.write(new)
        stream.truncate()
        stream.flush()
        os.fsync(stream.fileno())
    if target.read_text() != new:
        shutil.copyfile(backup, target)
        sys.exit('Weryfikacja zapisu nie powiodła się; przywrócono kopię.')
    subprocess.run(['restorecon', str(target)], check=True)
    print('Zapisano. Kopia:', backup)
    print('Cofnięcie: sudo cp --preserve=all', backup, target)
    print('Nie restartuj SDDM w aktywnej sesji. Sprawdź przy następnym logowaniu.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError) as exc:
        sys.exit(str(exc))
