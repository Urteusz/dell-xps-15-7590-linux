#!/usr/bin/env python3
"""Fedora 43 package plan, opt-in installation and offline bundle creation."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shlex
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / 'manifests/fedora-43.json').read_text())


def os_release():
    return platform.freedesktop_os_release()


def validate_host(info, model, arch):
    if info.get('ID') != 'fedora' or info.get('VERSION_ID') != MANIFEST['fedora_release']:
        raise ValueError('Obsługiwana instalacja: Fedora 43; inne wydania wymagają osobnego manifestu.')
    if model.strip() != MANIFEST['model'] or arch != MANIFEST['arch']:
        raise ValueError('Ten profil wymaga Dell XPS 15 7590 x86_64.')


def packages(profiles):
    return list(dict.fromkeys(p for profile in profiles for p in MANIFEST['profiles'][profile]))


def execute(command, apply):
    print('+ ' + shlex.join(command), flush=True)
    if apply:
        subprocess.run(command, check=True)


def bundle_hashes(directory):
    hashes = {}
    for package in sorted(directory.glob('*.rpm')):
        with package.open('rb') as stream:
            hashes[package.name] = hashlib.file_digest(stream, 'sha256').hexdigest()
    return hashes


def check_bundle(directory):
    data = json.loads((directory / 'bundle.json').read_text())
    if (data['fedora_release'], data['arch']) != ('43', 'x86_64'):
        raise ValueError('Paczka ma niewłaściwą dystrybucję lub architekturę.')
    actual = bundle_hashes(directory)
    if not actual or actual != data['sha256']:
        raise ValueError('Niekompletna lub zmieniona paczka RPM (SHA256).')
    return [str(directory / name) for name in sorted(actual)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['plan', 'install', 'download', 'offline-install'])
    parser.add_argument('--profiles', nargs='+', choices=list(MANIFEST['profiles']),
                        default=list(MANIFEST['profiles']))
    parser.add_argument('--apply', action='store_true', help='Wykonaj; domyślnie tylko plan')
    parser.add_argument('--directory', type=Path, default=ROOT / 'offline/fedora-43-x86_64')
    args = parser.parse_args()
    validate_host(os_release(), Path('/sys/class/dmi/id/product_name').read_text(), platform.machine())
    selected = packages(args.profiles)
    if args.action == 'plan':
        print('\n'.join(selected))
        return
    directory = args.directory.resolve()
    if args.action == 'offline-install':
        rpms = check_bundle(directory)
        # Hashes detect corruption, RPM signatures establish package provenance.
        execute(['sudo', 'dnf', '--disablerepo=*', '--setopt=localpkg_gpgcheck=True', '--setopt=install_weak_deps=False',
                 'install', *rpms], args.apply)
    else:
        if 'nvidia' in args.profiles:
            for name in ['rpmfusion-free-release', 'rpmfusion-nonfree-release']:
                if subprocess.run(['rpm', '-q', name], stdout=subprocess.DEVNULL).returncode:
                    raise ValueError('Najpierw skonfiguruj RPM Fusion według docs/INSTALL.md.')
        if args.action == 'install':
            execute(['sudo', 'dnf', 'install', *selected], args.apply)
        else:
            if args.apply:
                directory.mkdir(parents=True, exist_ok=True)
                if any(directory.iterdir()):
                    raise ValueError('Wybierz pusty katalog paczki; poprzednia zawartość pozostaje bez zmian.')
            execute(['dnf', '--setopt=install_weak_deps=False', 'download', '--resolve', '--alldeps',
                     '--destdir=' + str(directory), *selected], args.apply)
            if args.apply:
                hashes = bundle_hashes(directory)
                if not hashes:
                    raise ValueError('Brak pobranych RPM.')
                signature_check = subprocess.run(['rpmkeys', '--checksig', *[str(directory / name) for name in hashes]], capture_output=True, text=True)
                if signature_check.returncode:
                    raise ValueError('Weryfikacja podpisów RPM nie powiodła się. Sprawdź zaufane klucze Fedora/RPM Fusion; manifest kompletnej paczki nie został zapisany.')
                data = {k: MANIFEST[k] for k in ['fedora_release', 'arch', 'model']}
                data.update(profiles=args.profiles, sha256=hashes)
                (directory / 'bundle.json').write_text(json.dumps(data, indent=2) + '\n')
                print(f'Gotowa paczka: {directory} ({len(hashes)} RPM)')
    if args.action in ['install', 'offline-install']:
        print('Po instalacji NVIDIA: sudo akmods --force; sprawdź modinfo nvidia, potem uruchom ponownie system.')
        print('Secure Boot wymaga podpisu modułu i zapisania klucza MOK: docs/INSTALL.md.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as exc:
        sys.exit(str(exc))
