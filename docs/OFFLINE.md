# Offline installation

Prepare the bundle on Fedora 43 x86_64 with Fedora and RPM Fusion repositories enabled. The `dnf download` command requires `dnf5-plugins`.

```bash
python3 scripts/setup.py download
python3 scripts/setup.py download --apply
```

The output directory is `offline/fedora-43-x86_64/`. It contains RPM packages and `bundle.json` with package filenames and SHA256 checksums. Downloads include required dependencies even when already installed; weak dependencies are excluded. Allow several GB of free space.

Use an empty output directory. To retry an interrupted download without overwriting it:

```bash
python3 scripts/setup.py download --directory offline/retry --apply
```

Copy the repository and the complete bundle to the target laptop. Fedora and RPM Fusion signing keys must already be trusted on that system. Then run:

```bash
python3 scripts/setup.py offline-install
python3 scripts/setup.py offline-install --apply
```

For a custom directory, pass the same `--directory` option. The installer checks file hashes, disables remote repositories, and requires local RPM signature verification. Checksums detect corruption; package signatures establish provenance.

Bundles target the same Fedora release and architecture. An existing customized installation may have additional dependencies or conflicts. Boot the kernel installed by the bundle before validating its NVIDIA module. Goodix remains a separate source-based integration.

The reference bundle's 648 RPM files passed checksum and signature verification. A clean-system offline installation has not been tested. Binary bundles are not included in the Git repository.
