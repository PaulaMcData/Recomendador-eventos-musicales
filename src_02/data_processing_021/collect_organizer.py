import sys
import os
# Añade la ruta raíz del proyecto para poder importar módulos correctamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import unicodedata
import hashlib
from pymongo import MongoClient
from config_01 import MONGO_URI, DB_NAME

# Función para normalizar texto (sin tildes, en minúsculas y sin espacios innecesarios)
def normalize(text):
    if not text:
        return ""
    text = text.strip().lower()
    text = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("utf-8")
    return text

# Función para generar un id único a partir del nombre del organizador
def generate_organizer_id(name):
    return hashlib.md5(normalize(name).encode("utf-8")).hexdigest()

# Función principal que extrae organizadores únicos desde la colección 'events'
def collect_unique_organizers():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    events_collection = db["events"]
    organizers_collection = db["organizers"]

    unique_organizers = {}

    for event in events_collection.find():
        name = event.get("organizer", None)
        if not name:
            continue

        organizer_id = hashlib.md5(normalize(name).encode("utf-8")).hexdigest() if name else None

        if organizer_id and organizer_id not in unique_organizers:
            unique_organizers[organizer_id] = {
                "_id": organizer_id,
                "organizer": name
            }

    if unique_organizers:
        organizers_collection.delete_many({})
        organizers_collection.insert_many(unique_organizers.values())
        print(f"🎫 Organizadores guardados: {len(unique_organizers)}")
    else:
        print("ℹ️  No se encontraron organizadores únicos.")

if __name__ == "__main__":
    collect_unique_organizers()