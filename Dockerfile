# Imagem base oficial
FROM python:3.11

# Variáveis de ambiente (Formato sugerido: KEY=VALUE)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Atualiza o pip
RUN pip install --upgrade pip

# Instala as dependências do Python
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copia o código da aplicação
COPY . /app

# Variável de ambiente para a porta (Padrão 8000 se não definida)
ENV PORT=8000

# Expõe a porta dinâmica
EXPOSE $PORT

# Verificação de saúde do container
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:$PORT/ || exit 1

# Comando de execução usando python -m gunicorn
CMD python -m gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT
