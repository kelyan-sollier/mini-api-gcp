import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel, ChatSession

def initialize_vertex_ai():
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get("GCP_LOCATION", "us-central1")
    vertexai.init(project=project_id, location=location)

def generate_joke():
    initialize_vertex_ai()

    model = GenerativeModel(model_name="gemini-2.0-flash-001")
    chat = model.start_chat()

    prompt = "Raconte une blague originale et amusante en français, pour tout public (2 à 5 lignes)."
    response = chat.send_message(prompt)

    return response.text.strip()
