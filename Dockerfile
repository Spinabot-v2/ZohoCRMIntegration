FROM python:3.11-slim-bullseye AS base

WORKDIR /app
    
RUN apt-get update && apt-get install -y \
        build-essential libpq-dev gcc netcat-openbsd \
        && rm -rf /var/lib/apt/lists/*
    
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
    

# ----- Development stage -----
FROM base AS dev

COPY . .
    RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
  

# ----- Production stage -----
FROM base AS prod

COPY . .
RUN chmod +x /app/entrypoint.sh
    
ENTRYPOINT ["/app/entrypoint.sh"]