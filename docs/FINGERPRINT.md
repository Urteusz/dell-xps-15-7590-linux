# Goodix HTK32 27c6:5395 — eksperymentalny

Urządzenie nie występuje na sprawdzonej 2026-10-17 liście wspieranych urządzeń upstream libfprint. Na tym laptopie działa własna kompilacja libfprint 1.94.10 z rozszerzeniem Goodix53x5/SIGFM. Systemowy RPM `libfprint` ma inną wersję; sama lista RPM nie odzwierciedla biblioteki załadowanej przez usługę.

Usługa ma lokalny drop-in `/etc/systemd/system/fprintd.service.d/custom-libfprint.conf` ustawiający `LD_LIBRARY_PATH=/usr/local/lib64` i `G_MESSAGES_DEBUG=all`. Reguła `/etc/udev/rules.d/91-goodix-fingerprint.rules` odłącza `cdc_acm` od tego czytnika. Log potwierdza start niestandardowego sterownika. Nie kopiujemy wzorców palców ani obrazów z `/var/lib/fprint`.

## Zachowane źródła

`vendor/goodix53x5/` zawiera kopię lokalnego drzewa sterownika, łącznie ze zmianami użytkownika. Pochodzenie i dokładne commity: `provenance.json`. `local-driver.patch` dokumentuje zmiany już obecne w skopiowanych plikach — nie nakładaj go ponownie. `libfprint-integration.patch` to zmiany integracyjne lokalnego drzewa libfprint.

Odtworzenie drzewa do kompilacji, bez instalacji:

```bash
git clone https://gitlab.freedesktop.org/libfprint/libfprint.git build/libfprint
git -C build/libfprint checkout ee422fc3c5feae6e3bc290a23f0c625dcb934189
git -C build/libfprint apply ../../vendor/goodix53x5/libfprint-integration.patch
cp -r vendor/goodix53x5/drivers/goodix53x5 build/libfprint/libfprint/drivers/
cp -r vendor/goodix53x5/sigfm build/libfprint/libfprint/
```

Wymagania kompilacji: Meson, Ninja, kompilatory C/C++, GLib, libgusb, OpenSSL i OpenCV development oraz zależności wybranego zestawu libfprint. To materiał do odtworzenia eksperymentu, nie gotowy przetestowany RPM; główny instalator nie nadpisuje systemowego libfprint. W aktualnym upstream projektu Goodix są dalsze zmiany; snapshot zachowuje faktyczny lokalny stan, bez twierdzenia że jest najnowszy.

## Opóźnienie hasła i pierwsze logowanie

PAM w `/etc/pam.d/sddm` zawiera samodzielne `auth sufficient pam_fprintd.so` **przed** `password-auth`. Domyślny timeout modułu wynosi 30 s. PAM wykonuje ten stos kolejno, więc wpisane hasło czeka na zakończenie próby czytnika. W tej konfiguracji odczyt palca uruchamia się dopiero w trakcie próby logowania SDDM; samo dotykanie czytnika przed rozpoczęciem próby nie oznacza aktywnego skanowania. Blokada ekranu KDE ma osobny stos `kde-fingerprint`, dlatego jej zachowanie może być inne. Dokumentuje to lokalne `man pam_fprintd` i [zgłoszenie SDDM #1840](https://github.com/sddm/sddm/issues/1840).

Potwierdzona chronologia ostatniego startu:

- 23,219 s od startu: Claim urządzenia; 23,885 s: otwarcie zakończone.
- 23,894 s: rozpoczęcie weryfikacji; brak wykrytego dotknięcia w oczekiwaniu FDT.
- 53,890 s: timeout SDDM; 54,393 s: sesja użytkownika otwarta.
- 246,148 s: kolejna weryfikacja; 250,749 s: `verify-match`.

W trzech wcześniejszych rozruchach widać analogiczne timeouty 30 s; w jednym dwie próby. **Nie potwierdzono 3–4 minut ciągłego sprawdzania hasła**. Brak dotknięcia w logu nie rozstrzyga, czy użytkownik dotykał czujnika przed jego uzbrojeniem, czy sterownik nie wykrył dotknięcia po zimnym starcie. Potrzebny test fizyczny.

Przygotowana i zastosowana na badanym laptopie poprawka ogranicza pojedynczą próbę SDDM do 8 s i jednej próby. Nie naprawia samej przyczyny niewykrywania palca po zimnym starcie i nie gwarantuje 8 s całego logowania; czas dotyczy etapu weryfikacji modułu PAM.

```bash
python3 scripts/fix-login.py                 # pokaż dokładną zmianę
sudo python3 scripts/fix-login.py --apply    # kopia i zapis; wymaga hasła administratora
```

Alternatywa, gdy chcesz natychmiastowe logowanie hasłem i zachować odblokowanie KDE palcem: `sudo python3 scripts/fix-login.py --mode password --apply`. Usuwa próbę palca tylko z SDDM, pozostawiając `kde-fingerprint` i authselect. Nie uruchamiaj alternatywy po trybie password ponownie — skrypt celowo wymaga dokładnie jednej oczekiwanej reguły przed zmianą.

Nie restartuj SDDM podczas pracy — zakończyłoby to sesję. Test przy następnym normalnym uruchomieniu. Kopia i polecenie cofnięcia są wypisywane przez skrypt. Nie zmieniono generowanych przez authselect plików system-auth/password-auth.

## Test palca po zimnym starcie

1. Nie trzymaj palca na przycisku po włączeniu laptopa. Poczekaj na ekran logowania, rozpocznij próbę i dopiero wtedy przyłóż zapisany palec.
2. Zanotuj wynik i czas. Po zalogowaniu uruchom `python3 scripts/login-timeline.py`; pokazuje czasy etapów bez kont i surowych danych czytnika. Szczegóły: `journalctl -b -u sddm -u fprintd -o short-monotonic`.
3. Uruchom `fprintd-verify`, poczekaj na komunikat i przyłóż zapisany palec. Sprawdź też, że inny palec zostaje odrzucony. Nie wklejaj do publicznych raportów danych wzorców lub obrazów.
4. Porównaj pełne wyłączenie/włączenie z restartem i odblokowaniem ekranu. Dopiero takie wyniki pozwalają ocenić poprawkę sterownika.

SELinux zgłasza odmowy odczytu `nr_hugepages` przez fprintd; pojedyncze dopasowanie pomimo tego się powiodło. Nie dowodzi to przyczyny opóźnienia. Najpierw przeanalizuj AVC i etykiety biblioteki. Nie generuj bez przeglądu reguł `audit2allow` i nie wyłączaj SELinux. Dobór progów biometrycznych i instalacja nowego sterownika wymagają osobnej walidacji; snapshot nie jest rekomendacją do ochrony ważnych danych.

## Stan zastosowania poprawki

2026-10-17 zmieniono wyłącznie regułę czytnika w `/etc/pam.d/sddm` na `pam_fprintd.so timeout=8 max-tries=1`. Odczyt pliku po zapisie potwierdził zmianę; `authselect check` zwraca poprawną konfigurację. Kopia: `/var/backups/xps7590-login/sddm.20261017T100431216628Z`. Nie wykonano restartu ani pełnego testu logowania. Skrypt i przypadki odrzucające nieoczekiwane konfiguracje przeszły testy automatyczne.
