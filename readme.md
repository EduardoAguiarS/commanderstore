## Trabalho de Frameworks - Toledo Prudente 2023 Curso ADS

### Descrição ###
Trabalho realizado na materia de Frameworks, com o objetivo de criar uma aplicação web utilizando o framework Flask e MySQL.

### Requeriments ###
Python >= 3 e MySQL
1. ***blinker==1.6.2***
2. ***click==8.1.6***
3. ***Flask==2.3.2***
4. ***Flask-SQLAlchemy==3.0.5***
5. ***greenlet==2.0.2***
6. ***itsdangerous==2.1.2***
7. ***Jinja2==3.1.2***
8. ***MarkupSafe==2.1.3***
9. ***SQLAlchemy==2.0.19***
10. ***typing_extensions==4.7.1***
11. ***Werkzeug==2.3.6***

### Instalação Ubuntu/Debian ###
Instalar o pip
```bash
$ sudo apt install python3-pip
```
Instalar o virtualenv
```bash
$ sudo apt install python3-virtualenv
```
Definir o ambiente virtual
```bash
$ python3 -m venv venv
```
Ativar o ambiente virtual
```bash
$ source venv/bin/activate
```
Instalar os requeriments
```bash
$ pip install -r requirements.txt
```
### Execução ###
Exportar a variavel de ambiente FLASK_APP
```bash
$ export FLASK_APP=commanderstore.py
```
Executar o comando run
```bash
$ flask run
```
