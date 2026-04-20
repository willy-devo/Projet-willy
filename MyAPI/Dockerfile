# Image de base Python légère
FROM python:3.10-slim

# Définition du répertoire de travail dans le conteneur
WORKDIR /workdir

# Copie des fichiers de dépendances
COPY requirements.txt .

# Installation des bibliothèques nécessaires
RUN pip install --no-cache-dir -r requirements.txt

# Copie de l'intégralité du projet (app, catalog, agents)
COPY . .

# Exposition du port utilisé par FastAPI
EXPOSE 8000

# Commande pour lancer le serveur via Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]