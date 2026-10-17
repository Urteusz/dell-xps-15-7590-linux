# Testy funkcjonalne

`python3 scripts/diagnose.py --output reports/local.json` nie zmienia konfiguracji, nie rejestruje dźwięku ani obrazu, nie wykonuje logowania i nie usypia komputera. Kod wyjścia 1 oznacza wykryte ostrzeżenia; 0 nie oznacza pełnej sprawności. UNKNOWN oznacza brak dowodu, np. brak narzędzia lub ograniczone uprawnienia; MANUAL wymaga testu użytkowego. Uruchom w zwykłym terminalu sesji graficznej, nie przez sudo.

| Funkcja | Test ręczny | Kryterium |
|---|---|---|
| Audio | Odtwórz dźwięk w ustawieniach KDE; powtórz dla słuchawek | Oba kanały, brak trzasków, przełączenie wyjścia |
| Mikrofon | Nagraj próbkę w wybranej aplikacji | Czytelny zapis i właściwe źródło |
| Kamera | Otwórz podgląd w aplikacji kamery | Płynny obraz, poprawne zezwolenia |
| Bluetooth | Sparuj znane słuchawki lub mysz | Działa i łączy się ponownie |
| Touchpad | Ruch, tap, dwa/trzy palce przez kilka minut | Brak skoków; sprawdź logi KWin/libinput |
| Jasność i Fn | Regulacja jasności, głośności, klawisze funkcyjne | Poprawna reakcja i zakres |
| Uśpienie | Zapisz pracę, uśpij, wznowij; sprawdź Wi-Fi, audio, obie grafiki | Powtarzalne wznowienie; zapisz wybrane `/sys/power/mem_sleep` |
| HDMI/USB-C | Podłącz monitor; sprawdź obraz i dźwięk | Właściwa rozdzielczość, odłączanie i ponowne łączenie |
| Thunderbolt | Podłącz znaną stację i autoryzuj w KDE/bolt, jeśli wymagane | Monitor, USB i sieć stacji działają |
| SD | Użyj sprawnej karty testowej bez ważnych danych | Zapis/odczyt i bezpieczne wysunięcie; obecna karta ma błędy FAT |
| NVIDIA | PRIME OpenGL i następnie znana aplikacja 3D | Renderuje; brak nowych NV_ERR_NO_MEMORY lub Xid |
| Bateria | Obserwuj rozładowanie i ładowanie przy zwykłej pracy | Wiarygodny odczyt, brak niespodziewanych wyłączeń |
| Fingerprint | Zapisany palec i niewłaściwy palec po zimnym starcie | Poprawne dopasowanie i odrzucenie; patrz FINGERPRINT.md |

Nie wymuszaj trybu deep, undervoltingu, ręcznych wentylatorów lub blacklist bez odtworzenia konkretnego problemu. Hibernacja zależy również od swap i konfiguracji resume; nie jest automatycznie zapewniona przez pakiet sterowników.
