# Third-party code

The repository's own Python scripts, manifests and documentation are MIT licensed.

`vendor/goodix53x5/` is separate third-party work, declared by its upstream README as LGPL-2.1-or-later. See its `COPYING`, original source headers, upstream README credits and `provenance.json`. It includes Goodix protocol work and SIGFM code credited by upstream to Matthieu Charette, Natasha England-Elbro and Timur Mangliev. Local working-tree modifications are retained and documented in `local-driver.patch`; the copied driver already includes those changes. This project does not relicense that code under MIT or claim its authorship.

Fedora/RPM Fusion packages and vendor firmware retain their own licenses. They are not committed to Git. A downloaded binary bundle should retain its package metadata and be distributed according to each package's terms.
