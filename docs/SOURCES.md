# Źródła i pochodzenie

Sprawdzono 2026-10-17. Dowód lokalny jest podstawą raportu sprawności; opisy wsparcia na stronach nie zastępują testów tego egzemplarza.

- Dokumentacja producenta modelu: https://dl.dell.com/topicspdf/xps-15-7590-laptop_users-guide_en-us.pdf
- Dokumentacja sterownika Intel Wi-Fi i firmware: https://wireless.docs.kernel.org/en/latest/en/users/drivers/iwlwifi.html
- Dokumentacja wariantów modułu NVIDIA: https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/kernel-modules.html
- Lista urządzeń libfprint: https://fprint.freedesktop.org/supported-devices.html — na tej liście brak 27c6:5395; dotyczy wersji rozwojowej, nie gwarantuje zawartości RPM.
- Autor eksperymentalnego Goodix: https://github.com/AndyHazz/goodix53x5-libfprint — źródła lokalne pochodzą ze starszego commitu; dokładny snapshot w vendor/goodix53x5/provenance.json. Zachowano oryginalny README i kredyty SIGFM.
- SDDM i oczekiwanie na fingerprint przed hasłem: https://github.com/sddm/sddm/issues/1840 oraz zainstalowana dokumentacja `pam_fprintd(8)` (fprintd 1.94.5).
- RPM Fusion: https://rpmfusion.org/Howto/NVIDIA i https://rpmfusion.org/Howto/Secure%20Boot — podczas sprawdzania automatyczny dostęp zablokował Anubis, więc nie traktujemy ich treści jako odczytanej. Pakiety i składnię zweryfikowano lokalnie; aktualne instrukcje należy przeczytać przed zmianą gałęzi sterownika.
- Opcje pobierania pakietów: lokalne `dnf download --help` (DNF5), w tym `--resolve`, `--alldeps` i `--destdir`.

Dane lokalne: sysfs DMI/PCI/USB, lspci, lsusb, rpm, nvidia-smi, glxinfo (Intel i PRIME), nmcli bez SSID, wpctl, bluetoothctl, journalctl, fwupdmgr get-devices. Publiczny raport zawiera tylko wybrane ustalenia, bez surowych identyfikatorów urządzeń.
