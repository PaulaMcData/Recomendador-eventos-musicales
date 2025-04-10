import os
import sys
# Añade la ruta raíz del proyecto para poder importar módulos correctamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import unicodedata
import hashlib
from pymongo import MongoClient
from config_01 import MONGO_URI, DB_NAME

# Normaliza un string eliminando acentos, espacios y pasando a minúsculas
def normalize_text(text):
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    return text.strip().lower()

# Conexión a la base de datos MongoDB
def connect_to_db():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]

# Genera un id único en formato hash a partir del nombre del artista normalizado
def generate_artist_id(normalized_name):
    return hashlib.md5(normalized_name.encode()).hexdigest()

# Extrae artistas únicos desde la colección "events" y los guarda en "artists"
def collect_unique_artists():
    db = connect_to_db()
    events = db["events"].find()
    artists_collection = db["artists"]

    unique_names = set()

    for event in events:
        name = event.get("artist")
        if name:
            unique_names.add(name)

    for name in unique_names:
        normalized_name = normalize_text(name)
        artist_doc = {
            "_id": generate_artist_id(normalized_name),
        "artist": name
        }
        if not artists_collection.find_one({"_id": artist_doc["_id"]}):
            artists_collection.insert_one(artist_doc)
            print(f"🎤 Artista guardado: {artist_doc['artist']}")
        else:
            print(f"✅ Artista existente: {artist_doc['artist']}")

# Permite ejecutar el script individualmente desde el debugger o terminal
if __name__ == "__main__":
    collect_unique_artists()
