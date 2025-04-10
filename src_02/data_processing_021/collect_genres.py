import os
import sys
# Añade la ruta raíz del proyecto para poder importar módulos correctamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import unicodedata
import hashlib
from pymongo import MongoClient
from config_01 import MONGO_URI, DB_NAME

# Establece la conexión con MongoDB
def connect_to_db():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]

# Normaliza el texto para comparación y generación de ID
def normalize(text):
    if not text:
        return ""
    text = text.strip().lower()
    text = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("utf-8")
    return text

# Genera un identificador único basado en género y subgénero
def generate_genre_id(genre_name, subgenre_name):
    return hashlib.md5(f"{normalize(genre_name)}_{normalize(subgenre_name)}".encode("utf-8")).hexdigest() if genre_name and subgenre_name else None

# Se recogen y guardan combinaciones únicas de género y subgénero
def collect_unique_genres():
    db = connect_to_db()
    events = db["events"].find()
    genres_collection = db["genres"]

    unique_genres = set()

    # Recolectar todas las combinaciones únicas de género y subgénero de la colección "events"
    for event in events:
        genre = event.get("genre")
        subgenre = event.get("subgenre")
        if genre:
            unique_genres.add((genre, subgenre))

    # Insertar en la colección "genres" si no existen ya por su id
    for genre_name, subgenre_name in unique_genres:
        genre_name = str(genre_name).strip()
        subgenre_name = str(subgenre_name).strip() if subgenre_name else None
        genre_id = generate_genre_id(genre_name, subgenre_name)
        existing_doc = genres_collection.find_one({"_id": genre_id})

        if not existing_doc:
            genre_doc = {
                "_id": genre_id,
                "genre": genre_name,
                "subgenre": subgenre_name
            }
            genres_collection.insert_one(genre_doc)
            print(f"🎶 Nuevo género guardado: {genre_name} - Subgénero: {subgenre_name}")
        else:
            print(f"✅ Género y subgénero ya existentes: {genre_name} - {subgenre_name}")

if __name__ == "__main__":
    collect_unique_genres()
