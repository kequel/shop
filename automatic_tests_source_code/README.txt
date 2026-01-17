>>> >>> >>> AKTYWACJA SRODOWISKA I INSTALACJA PLUGINOW <<< <<< <<<

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt



>>> >>> >>> URUCHOMIENIE TESTOWANIA <<< <<< <<<

Graficzny Chrome (DOMYSLNIE): >>> pytest
Graficzny Firefox:            >>> pytest --browser=firefox

Headless Chrome:              >>> pytest --headless
Headless Firefox:             >>> pytest --browser=firefox --headless



>>> >>> >>> URUCHOMIENIE TESTOWANIA NA SKLEPIE NA KLASTRZE <<< <<< <<<

1. Otworzyc dwa okna wsl ubuntu

2. W pierwszym oknie, wejść do folderu ze skryptem testującym (cd ~/Shop/automatic_tests_source_code).

3. W drugim oknie, wejść do "~/Shop"
3.1 Wpisac "ssh -J rsww@172.20.83.101 -L 19665:127.0.0.1:19665 hdoop@10.40.71.115"
3.2 Jeśli zacznie zadawać pytania o authenticity, wpisac "yes" za każdym razem
3.3 Efekt końcowy: widoczne "hdoop@student-swarm01:~$" (wlaczylismy tunelowanie, ale dla ubuntu) UWAGA: TEGO OKNA NIE ZAMYKAMY!!!!!!!!!!!!!

4. Wrocic do pierwszego okna wsl ze skryptem testującym
4.1 Uruchomic pytest (klasycznie, jak to było na I etapie [instrukcja wyżej])



>>> >>> >>> DODAC W .GITIGNORE <<< <<< <<<

#Python
venv/
__pycache__
.pytest_cache