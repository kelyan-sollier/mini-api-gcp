from vertexai.preview.generative_models import GenerativeModel
import vertexai

vertexai.init(project="mini-projet-data-tools", location="us-central1")
response = model.generate_content("Raconte-moi une blague.")
model = GenerativeModel("gemini-1.5-flash")  # ou gemini-1.5-pro

print(response.text)
