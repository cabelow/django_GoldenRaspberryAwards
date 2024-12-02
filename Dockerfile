# Use a imagem oficial do Python 3.11 como base
FROM python:3.11

# Defina o diretório de trabalho
WORKDIR /app

# Copie o arquivo de dependências e instale os pacotes necessários
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante da aplicação
COPY . .

# Exponha a porta 8000 para acesso externo
EXPOSE 8000

# Comando para rodar o servidor Django em produção
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
