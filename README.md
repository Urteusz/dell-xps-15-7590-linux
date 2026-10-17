# Dell XPS 15 7590 — Linux kit

Zestaw instalacyjny i diagnostyczny dla **Dell XPS 15 7590**, przygotowany na fizycznym laptopie z **Fedora 43 KDE, Intel i7-9750H, UHD 630, GTX 1650, Killer AX1650x / Intel AX200**. Dokumentacja po polsku. Stan weryfikacji: **2026-10-17**.

Sterowniki większości urządzeń dostarcza kernel Linux. Repozytorium zawiera manifest pakietów, instalator, generator paczki RPM offline, diagnostykę oraz zachowaną eksperymentalną wersję sterownika Goodix. Nie jest uniwersalnym instalatorem dla wszystkich dystrybucji ani gwarancją działania każdego wariantu 7590.

## Szybki start

W katalogu repozytorium, jako zwykły użytkownik:

```bash
python3 scripts/diagnose.py --output reports/local.json
python3 scripts/setup.py plan
python3 scripts/setup.py install            # pokazuje polecenie
python3 scripts/setup.py install --apply    # instalacja z potwierdzeniem DNF
```

Instalator sprawdza model, architekturę i wersję Fedory. Profil domyślny obejmuje bazę, NVIDIA i narzędzia. Wymaga skonfigurowanego RPM Fusion dla NVIDIA: [instalacja](docs/INSTALL.md). Na obecnej maszynie sterowniki już są zainstalowane; nie trzeba ich instalować ponownie do wykonania diagnostyki.

## Zawartość

- [Wykryty sprzęt i sterowniki](hardware/7590.md).
- [Rzeczywisty raport z laptopa](docs/VERIFIED-2026-10-17.md), z problemami i granicami testów.
- [Instalacja, Secure Boot i powrót do poprzedniego kernela](docs/INSTALL.md).
- [Paczka offline](docs/OFFLINE.md): RPM z zależnościami, wersjami i SHA256.
- [Goodix 27c6:5395](docs/FINGERPRINT.md): lokalne źródła, pochodzenie i zmiany; instalacja eksperymentalna poza instalatorem głównym.
- [Testy ręczne](docs/TESTING.md): audio, kamera, suspend, Bluetooth i złącza.
- [Źródła informacji](docs/SOURCES.md).

**Poprawka logowania:** po zgłoszeniu opóźnienia skrócono oczekiwanie SDDM na palec do 8 s i jednej próby; test po restarcie pozostaje do wykonania. Szczegóły i kopia konfiguracji w [FINGERPRINT.md](docs/FINGERPRINT.md).

**Nie wszystko można oznaczyć jako sprawne:** NVIDIA ma historyczne błędy pamięci, touchpad zgłasza skoki, a fprintd napotyka odmowy SELinux. Kamera, mikrofon, uśpienie i urządzenia zewnętrzne wymagają testów użytkowych. Raport odróżnia wykrycie sterownika od pełnego testu funkcji.

## Publikacja na GitHubie

Repozytorium jest lokalne, bez remote. `offline/`, `reports/` i katalogi kompilacji są ignorowane. Przygotowana lokalna paczka offline zawiera 648 RPM i zajmuje około 1,2 GB. Paczki RPM mogą zajmować dużo miejsca — udostępniaj je osobno jako archiwum lub Release po sprawdzeniu warunków dystrybucji pakietów. Kod główny: MIT; źródła `vendor/goodix53x5/` mają odrębne warunki LGPL i zachowane autorstwo. Zobacz [THIRD_PARTY.md](THIRD_PARTY.md).

Sprawdzenie skryptów: `python3 -m unittest discover -s tests -v`.
