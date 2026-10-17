#!/usr/bin/env python3
"""Show only authentication stage timings, without fingerprint templates or account names."""
import argparse
import json
import subprocess
import sys

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--boot', default='0', help='0 = obecny rozruch, -1 = poprzedni')
args = p.parse_args()
result = subprocess.run(['journalctl', '-b', args.boot, '-u', 'sddm', '-u', 'fprintd',
                         '-o', 'json', '--no-pager'], capture_output=True, text=True)
if result.returncode:
    sys.exit('Nie można odczytać dziennika rozruchu; sprawdź uprawnienia i numer boot.')
markers = [('Device reported open completion', 'Czytnik otwarty'),
           ('start verification device', 'Start weryfikacji palca'),
           ('Verification timed out', 'Timeout weryfikacji w SDDM'),
           ('report_verify_status: result verify-match', 'Poprawne dopasowanie'),
           ('report_verify_status: result verify-no-match', 'Brak dopasowania / anulowanie'),
           ('pam_unix(sddm:session): session opened', 'Otwarcie sesji KDE')]
for line in result.stdout.splitlines():
    row = json.loads(line)
    message = row.get('MESSAGE', '')
    for marker, label in markers:
        if marker in message:
            seconds = int(row['__MONOTONIC_TIMESTAMP']) / 1e6
            print(f'{seconds:10.3f} s  {label}')
