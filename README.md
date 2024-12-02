# Django Project with Docker

Este projeto Django está configurado para ser executado em um contêiner Docker. Siga os passos abaixo para configurar e iniciar o projeto.

## Pré-requisitos

- **Docker**: [Instale o Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Instale o Docker Compose](https://docs.docker.com/compose/install/)

## Clonando o Projeto

Clone o repositório para sua máquina local:

```bash
git clone https://github.com/cabelow/django_GoldenRaspberryAwards.git
cd django_GoldenRaspberryAwards
```


Comandos Docker:
para instalar as libs antes de rodar o projeto
sudo docker-compose run web pip install -r requirements.txt
para rodar o projeto:
sudo docker-compose build
sudo docker-compose up
sudo docker-compose up --build
para rodar migrante se necessario:
docker-compose run web python manage.py migrate



## Instalação do Python

Para rodar o projeto localmente fora do Docker, você precisará ter o Python 3.x instalado em sua máquina. Recomenda-se a versão **Python 3.11** ou superior. Siga as instruções abaixo para instalar o Python:

alguns comandos para ajudar com o Python para ubuntu:

```bash
sudo apt update
sudo apt install python3
python3 --version
sudo apt install python3-pip
```

Instalando as dependencias do projeto:
pip install -r requirements.txt


Depois de tudo instalado você pode:

rodar os testes:
python3 -m pytest


Para acessar o Admin do Django:
http://0.0.0.0:8000/admin/
django_admin: Golden_Raspberry
senha: Golden_Raspberry

Para usar o Postman login
user_auth:Raspberry
senha: Wyyk@PGiQCewCT9
tem um arquivo chamado "GoldenRaspberryAwards.postman_collection.json"
nele contem a collection do Postman para uso

para acessar a documentação:
http://0.0.0.0:8000/swagger/

qualquer duvida fico a disposição.