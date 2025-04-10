import os
import sys
# Asegura que el script pueda importar módulos desde la raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import unicodedata
import hashlib
from pymongo import MongoClient
from config_01 import MONGO_URI, DB_NAME

# Genera un hash MD5 único a partir de un texto
def generate_md5_hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

# Normaliza el texto: elimina acentos, espacios y convierte a minúsculas
def normalize_text(text):
    if not text:
        return ""
    text = text.strip().lower()
    text = unicodedata.normalize('NFKD', text)
    text = ''.join(c for c in text if not unicodedata.combining(c))
    return text

# Extrae y guarda lugares únicos de la colección de eventos en MongoDB
def collect_unique_places():
    # Conexión a la base de datos MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    
    events_collection = db["events"]
    places_collection = db["places"]

    # Diccionario para almacenar lugares únicos con su id
    unique_places = {}
    
    # Recorre todos los eventos y extrae los datos del lugar
    for event in events_collection.find():
        location = event.get("location", {})
        place_name = location.get("place")

        if place_name:
            key = f"{normalize_text(location.get('city', ''))}_{normalize_text(location.get('country', ''))}"
            city_id = generate_md5_hash(key)
            unique_id = generate_md5_hash(normalize_text(place_name) + "_" + city_id)

            if unique_id not in unique_places:
                place_doc = {
                    "_id": unique_id,
                    "name": place_name,
                    "latitude": location.get("latitude"),
                    "longitude": location.get("longitude"),
                    "address": location.get("address"),
                    "postalCode": location.get("postalCode"),
                    "city_id": city_id
                }
                unique_places[unique_id] = place_doc

    # Inserta o actualiza los documentos únicos de lugar en la colección 'places'
    if unique_places:
        inserted_count = 0
        updated_count = 0
        for place_id, place_doc in unique_places.items():
            result = places_collection.update_one(
                {"_id": place_id},
                {"$set": place_doc},
                upsert=True
            )
            if result.upserted_id:
                inserted_count += 1
            elif result.modified_count:
                updated_count += 1
        print(f"🏟️ 'places' actualizado: {inserted_count} insertados, {updated_count} modificados.")
    else:
        print("⚠️ No se encontraron lugares únicos.")

if __name__ == "__main__":
    collect_unique_places()
