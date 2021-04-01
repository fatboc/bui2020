# BUI2020
Przykładowa aplikacja wykonana w ramach kursu.

### Uruchomienie aplikacji

Aplikacja uruchamiana jest w ramach klastra kubernetes. Skrypt [start.sh](start.sh) ma za zadanie zbudować zdefiniowane obrazy oraz utworzyć odpowiednie zasoby w klastrze.

### Struktura aplikacji

Działanie aplikacji jest realizowane poprzez trzy deploymenty z obrazami
* jaeger:all-in-one
* bazą danych mysql
* aplikacji realizowanej we frameworku flask umożliwiającej dostęp do zapisanych danych
Aby umożliwić komunikację między podami zdefiniowane zostały również odpowiednie serwisy.
