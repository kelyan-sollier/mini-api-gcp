# 🌐 Mini API GCP

Ce projet est une mini-API construite avec Flask et déployée sur **Google Cloud Run**. Elle permet :
- 🔍 De consulter le statut du serveur
- 📥 De stocker et lire des données depuis un bucket Google Cloud Storage
- 😂 De générer une blague en français via **Vertex AI Gemini**

---

## 🚀 Routes disponibles

| Méthode | Endpoint     | Description                              |
|--------:|--------------|------------------------------------------|
| `GET`   | `/hello`     | Retourne un message de bienvenue         |
| `GET`   | `/status`    | Donne l’heure du serveur + statut        |
| `GET`   | `/data`      | Récupère les données stockées dans GCS   |
| `POST`  | `/data`      | Envoie de nouvelles données à GCS        |
| `GET`   | `/joke`      | Génère une blague originale en français  |

---

## 🛠 Technologies utilisées

- Python 3.10
- Flask
- Vertex AI (Gemini 1.5 Flash)
- Google Cloud Storage
- Docker
- Google Cloud Run

---

## 🧪 Tests locaux

```bash
docker build -t mini-api-gcp .
docker run -p 8080:8080 \
  --env GCP_PROJECT_ID=mini-projet-data-tools \
  --env GCP_LOCATION=us-central1 \
  --env GCS_BUCKET_NAME=mini_projet_data-tools_bucket12 \
  --env GCS_FILE_PATH=data/storage.json \
  --env GCS_FILE_FORMAT=json \
  -v "$(pwd)/service-account-key.json:/app/service-account-key.json" \
  mini-api-gcp



#API disponible sur http://localhost:8080


## Déploiement sur Google Cloud Run


gcloud builds submit --tag gcr.io/mini-projet-data-tools/mini-api-gcp

gcloud run deploy mini-api-gcp \
  --image gcr.io/mini-projet-data-tools/mini-api-gcp \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GCP_PROJECT_ID=mini-projet-data-tools,GCP_LOCATION=us-central1,GCS_BUCKET_NAME=mini_projet_data-tools_bucket12,GCS_FILE_PATH=data/storage.json,GCS_FILE_FORMAT=json
