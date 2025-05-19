# Utiliser une image Python officielle légère
FROM python:3.10-slim

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code
COPY . .

# Copier la clé de compte de service dans le conteneur
COPY service-account-key.json /app/service-account-key.json

# Définir la variable d’environnement pour l’authentification GCP
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/service-account-key.json"

# Éviter le buffering des logs
ENV PYTHONUNBUFFERED=1

# Exposer le port 8080
EXPOSE 8080

# Lancer l’application avec Gunicorn
CMD ["gunicorn", "--bind", ":8080", "--workers", "1", "--threads", "8", "app.main:app"]
