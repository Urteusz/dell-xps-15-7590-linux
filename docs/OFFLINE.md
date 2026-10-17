# Paczka RPM offline

Repozytorium Git zawiera przepisy i źródła Goodix. Binaria Fedory i NVIDIA są pobierane osobno do ignorowanego katalogu `offline/`. Przygotuj paczkę na Fedora 43 x86_64 z włączonymi repozytoriami Fedora i RPM Fusion:

```bash
python3 scripts/setup.py download
python3 scripts/setup.py download --apply
```

Wymagany jest podrozkaz `dnf download` (pakiet `dnf5-plugins`). `--resolve --alldeps` pobiera także zależności już obecne na maszynie przygotowującej paczkę. Słabe zależności są wyłączone podczas pobierania. Przygotowanie może zużyć kilka GB. Otrzymujesz `offline/fedora-43-x86_64/*.rpm` i `bundle.json` z dokładnymi nazwami plików oraz SHA256. Nie kopiuj samych RPM bez manifestu. Przy błędzie pobierania katalog nie jest kompletną paczką; ponów w nowym pustym katalogu przez `--directory`.

Skopiuj repozytorium i katalog offline na docelowy laptop, potem:

```bash
python3 scripts/setup.py offline-install
python3 scripts/setup.py offline-install --apply
```

Instalacja sprawdza sumy plików, wyłącza zdalne repozytoria i wymaga weryfikacji podpisów lokalnych RPM przez DNF. Klucze Fedora/RPM Fusion muszą już być zaufane w systemie docelowym; skonfiguruj je przed odłączeniem sieci. SHA256 wykrywa uszkodzenie pliku, ale nie zastępuje podpisu wydawcy. Nie obchodź błędu zaufania przez `--nogpgcheck`.

Pakiet jest przeznaczony dla tej samej wersji Fedory i architektury. Zmodyfikowany system docelowy może mieć dodatkowe zależności lub konflikty. Pobieranie sprawdza kompletność plików, ale pełną instalację offline trzeba sprawdzić na czystej Fedora 43; na używanym laptopie jej nie wykonano.

Pakiety kernela i `kernel-devel-matched` są pobierane z aktualnych repozytoriów. Po instalacji uruchom nowo zainstalowany kernel. Nie oczekuj zgodności z dawnym kernelem, dla którego repozytoria nie udostępniają już nagłówków. Goodix pozostaje osobnym eksperymentalnym źródłem, nie jest częścią transakcji RPM.

## Paczka przygotowana na tym laptopie

2026-10-17 pobrano **648 RPM** do `offline/fedora-43-x86_64/` (około 1,2 GB). Pakiety pochodzą z dostępnych w chwili pobierania repozytoriów, więc nie muszą mieć tych samych wersji co aktualnie uruchomiony system. `bundle.json` zawiera pełną listę i SHA256. Wykonano kontrolę sum oraz podpisów RPM. Nie przeprowadzono instalacji na czystym systemie ani restartu do kernela z paczki. Pliki binarne pozostają lokalne i są ignorowane przez Git.
