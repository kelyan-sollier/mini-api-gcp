import os
import json
import csv
import io
from google.cloud import storage

# Récupérer les variables d'environnement
BUCKET_NAME = os.environ.get('GCS_BUCKET_NAME')
FILE_PATH = os.environ.get('GCS_FILE_PATH')
FILE_FORMAT = os.environ.get('GCS_FILE_FORMAT', 'json')  # 'json' ou 'csv'

def get_storage_client():
    """Initialise et retourne un client Google Cloud Storage"""
    return storage.Client()

def read_from_gcs():
    """Lit les données depuis Google Cloud Storage"""
    client = get_storage_client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(FILE_PATH)
    
    if not blob.exists():
        # Si le fichier n'existe pas, retourne une structure vide
        return [] if FILE_FORMAT == 'json' else {"headers": [], "rows": []}
    
    content = blob.download_as_string()
    
    if FILE_FORMAT == 'json':
        # Traitement pour JSON
        data = json.loads(content)
        return data
    elif FILE_FORMAT == 'csv':
        # Traitement pour CSV
        csv_content = content.decode('utf-8')
        csv_file = io.StringIO(csv_content)
        reader = csv.reader(csv_file)
        
        rows = list(reader)
        if rows:
            headers = rows[0]
            data_rows = rows[1:]
            return {"headers": headers, "rows": data_rows}
        else:
            return {"headers": [], "rows": []}
    else:
        raise ValueError(f"Format de fichier non supporté: {FILE_FORMAT}")

def write_to_gcs(data):
    """Écrit des données dans Google Cloud Storage"""
    client = get_storage_client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(FILE_PATH)
    
    # Vérifier si le fichier existe déjà pour l'ajout de données
    existing_data = []
    if blob.exists():
        if FILE_FORMAT == 'json':
            existing_content = blob.download_as_string()
            existing_data = json.loads(existing_content)
    
    if FILE_FORMAT == 'json':
        # Traitement pour JSON
        if isinstance(existing_data, list):
            existing_data.append(data)
        else:
            # Si ce n'est pas une liste, initialiser avec la nouvelle donnée
            existing_data = [data]
        
        updated_content = json.dumps(existing_data, indent=2)
        blob.upload_from_string(updated_content, content_type='application/json')
        return {"added": True, "total_records": len(existing_data)}
    
    elif FILE_FORMAT == 'csv':
        # Traitement pour CSV
        # Lire le fichier existant pour obtenir les en-têtes
        existing_rows = []
        headers = []
        
        if blob.exists():
            csv_content = blob.download_as_string().decode('utf-8')
            reader = csv.reader(io.StringIO(csv_content))
            rows = list(reader)
            if rows:
                headers = rows[0]
                existing_rows = rows[1:]
        
        # Si les en-têtes n'existent pas, les extraire des clés de données
        if not headers and isinstance(data, dict):
            headers = list(data.keys())
        
        # Préparer la nouvelle ligne
        if isinstance(data, dict):
            new_row = [data.get(header, "") for header in headers]
        elif isinstance(data, list):
            new_row = data
        else:
            raise ValueError("Format de données incorrect pour CSV")
        
        # Ajouter la nouvelle ligne
        existing_rows.append(new_row)
        
        # Réécrire le fichier complet
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(headers)
        writer.writerows(existing_rows)
        
        blob.upload_from_string(output.getvalue(), content_type='text/csv')
        return {"added": True, "total_records": len(existing_rows)}
    
    else:
        raise ValueError(f"Format de fichier non supporté: {FILE_FORMAT}")
