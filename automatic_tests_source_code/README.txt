>>> >>> >>> AKTYWACJA SRODOWISKA I INSTALACJA PLUGINOW <<< <<< <<<

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt



>>> >>> >>> URUCHOMIENIE TESTOWANIA <<< <<< <<<

Graficzny Chrome (DOMYSLNIE): >>> pytest
Graficzny Firefox:            >>> pytest --browser=firefox

Headless Chrome:              >>> pytest --headless
Headless Firefox:             >>> pytest --browser=firefox --headless



>>> >>> >>> DODAC W .GITIGNORE <<< <<< <<<

#Python
venv/
__pycache__
.pytest_cache