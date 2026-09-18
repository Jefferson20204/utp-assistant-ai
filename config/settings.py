import os
from types import SimpleNamespace
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY or GEMINI_API_KEY == "tu_api_key_aqui":
    print("[ADVERTENCIA] Por favor, configura tu GEMINI_API_KEY real en el archivo .env")

settings = SimpleNamespace(GEMINI_API_KEY=GEMINI_API_KEY)