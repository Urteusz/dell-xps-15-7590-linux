# Instalacja na Fedora 43 x86_64

Wymagane: Python 3, DNF5, działająca Fedora 43. Uruchamiaj skrypty jako zwykły użytkownik; tylko instalacja wywołuje `sudo`. Domyślnie skrypt wyświetla plan, a `--apply` wykonuje operację. DNF zachowuje własne potwierdzenie transakcji.

## Repozytoria NVIDIA

Gdy RPM Fusion nie jest jeszcze skonfigurowane, zapoznaj się z aktualnymi instrukcjami https://rpmfusion.org/Configuration i https://rpmfusion.org/Howto/NVIDIA. Przykład dla wydania 43:

```bash
sudo dnf install https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-43.noarch.rpm https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-43.noarch.rpm
```

## Pakiety

```bash
python3 scripts/setup.py plan
python3 scripts/setup.py install --apply
```

Tylko baza i narzędzia, bez pakietów NVIDIA:

```bash
python3 scripts/setup.py install --profiles base tools --apply
```

Nie są dodawane parametry GRUB, blacklisty, ręczne sterowanie wentylatorami ani usługi zarządzania energią. Zastana instalacja korzysta z tuned/tuned-ppd i thermald; ich dobór jest konfiguracją systemu, nie brakującym sterownikiem. Nie dokładaj TLP bez sprawdzenia konfliktów z istniejącą konfiguracją.

## Po instalacji NVIDIA

```bash
sudo akmods --force
modinfo -F version nvidia
modinfo -F vermagic nvidia
uname -r
```

Poczekaj na zakończenie budowy akmods. Wersja modułu na dysku nie dowodzi jego załadowania. Po zmianie kernela lub sterownika uruchom system ponownie w dogodnym momencie, a następnie:

```bash
nvidia-smi
python3 scripts/diagnose.py --output reports/after-install.json
```

Test PRIME:

```bash
__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia glxinfo -B
```

Na badanej maszynie pakiet `akmod-nvidia` dostarcza załadowany moduł Open Kernel Module 580.178.04 (`Dual MIT/GPL`), co potwierdzono w logu i modinfo. Nie zamieniaj automatycznie go na inny wariant wyłącznie na podstawie nazwy pakietu.

## Secure Boot

W czasie audytu był wyłączony. Włączenie go wymaga podpisania modułu NVIDIA i zaufanego klucza. Sprawdź `mokutil --sb-state` i instrukcję RPM Fusion: https://rpmfusion.org/Howto/Secure%20Boot oraz lokalny `/usr/share/doc/akmods/README.secureboot`. Nie wyłączaj Secure Boot jako automatycznego obejścia. Instalator nie zapisuje kluczy ani nie zmienia UEFI.

## Powrót po problemach

Wybierz poprzedni działający kernel w menu startowym. Nie usuwaj go przed sprawdzeniem nowego. Sprawdź `dnf history list` i `dnf history info <ID>`; ewentualne cofnięcie transakcji wymaga przeglądu zależności i dostępności poprzednich pakietów. Repozytorium nie modyfikuje plików `/etc`, więc nie ma dodatkowych ukrytych zmian do wycofania.
