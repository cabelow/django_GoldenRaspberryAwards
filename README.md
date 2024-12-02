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

## Comandos Docker

### Instalando dependências antes de rodar o projeto:
```bash
sudo docker-compose run web pip install -r requirements.txt
```

### Rodando o projeto:
```bash
sudo docker-compose build
sudo docker-compose up
```
Ou combine os passos:
```bash
sudo docker-compose up --build
```

### Rodando migrações, se necessário:
```bash
docker-compose run web python manage.py migrate
```

## Instalação do Python

Para rodar o projeto localmente fora do Docker, você precisará ter o Python 3.x instalado em sua máquina. Recomenda-se a versão **Python 3.11** ou superior. Siga as instruções abaixo para instalar o Python:

### Comandos para ajudar com o Python no Ubuntu:
```bash
sudo apt update
sudo apt install python3
python3 --version
sudo apt install python3-pip
```

### Instalando as dependências do projeto:
```bash
pip install -r requirements.txt
```

## Executando Testes

Para rodar os testes:
```bash
python3 -m pytest
```

## Acessando o Admin do Django

URL: [http://0.0.0.0:8000/admin/](http://0.0.0.0:8000/admin/)

Credenciais de acesso:
- **Usuário**: Golden_Raspberry
- **Senha**: Golden_Raspberry

## Usando o Postman

Para autenticação no Postman:
- **Usuário**: Raspberry
- **Senha**: Wyyk@PGiQCewCT9

Há um arquivo chamado `GoldenRaspberryAwards.postman_collection.json` que contém a coleção do Postman para facilitar o uso da API.

## Documentação da API

A documentação Swagger está disponível em:
[http://0.0.0.0:8000/swagger/](http://0.0.0.0:8000/swagger/)

Qualquer dúvida, fico à disposição.
