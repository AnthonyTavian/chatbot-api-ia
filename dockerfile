# Usa Python 3.11 slim (versão leve)
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Copia requirements primeiro (cache de layers)
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Expõe a porta 8000
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]