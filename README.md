#BUI2020

###Uruchomienie aplikacji

Aplikacja uruchamiana jest jako klaster kubernetes w środowisku minikube. Skrypt [start.sh](start.sh) ma za zadanie utworzyć odpowiednie usługi w klastrze. 

###Struktura aplikacji

Działanie aplikacji jest realizowane poprzez trzy deploymenty z obrazami
* jaeger:all-in-one
* bazą danych mysql
* aplikacji realizowanej we frameworku flask
Aby umożliwić komunikację 
