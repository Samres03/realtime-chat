FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Dependencias de sistema (psycopg, builds, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl \
  && rm -rf /var/lib/apt/lists/*

# Instala uv (rápido y simple)
RUN pip install --no-cache-dir uv

# Copiamos solo los metadatos primero para aprovechar cache
COPY pyproject.toml uv.lock* ./

# Crea venv y sincroniza deps del lock
RUN uv sync --frozen

# Copiamos el código
COPY app ./app

EXPOSE 8000

# Comando base (sin --reload; para dev se sobreescribe en compose)
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
