# Репозиторий с исходным кодом бэк-энда GreenAppleSite

## Развернуть проект

### Локально

1. Установить виртуальное окружение

* ```sudo apt-get update && sudo apt-get -y upgrade```
* ```sudo-apt-get install -y python3-venv```
* ```python3 -m venv venv```
* ```. venv/bin/acivate```
* ```pip install -r requirements.txt```  
Запустить проект  
* ```uvicorn app:app --reload```

### В Docker-compose

* ```docker-compose build```  
Запустить проект 
* ```docker-compose up```