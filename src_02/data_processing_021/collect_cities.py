import os
import sys
# Añade la ruta raíz del proyecto para poder importar módulos correctamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import unicodedata
import hashlib
from pymongo import MongoClient
from config_01 import MONGO_URI, DB_NAME

# Función para generar un ID único para cada ciudad usando MD5 (normaliza acentos y convierte a minúsculas)
def generate_city_id(city_name, country):
    city_name = unicodedata.normalize('NFKD', city_name).encode('ASCII', 'ignore').decode('utf-8').strip().lower()
    country = unicodedata.normalize('NFKD', country).encode('ASCII', 'ignore').decode('utf-8').strip().lower()
    raw_string = f"{city_name}_{country}"
    return hashlib.md5(raw_string.encode('utf-8')).hexdigest()

# Función principal para recolectar ciudades únicas desde 'events' y generar id únicos
def collect_unique_cities():
    """
    Extrae ciudades únicas desde la colección 'events', genera IDs únicos
    y actualiza la colección 'cities' sin insertar duplicados.
    """
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    # Agrupar por ciudad y país desde la colección 'events'
    pipeline = [
        {"$group": {"_id": {"city": "$location.city", "country": "$location.country"}}},
        {"$project": {"_id": 0, "city": "$_id.city", "country": "$_id.country"}},
        {"$sort": {"country": 1, "city": 1}}
    ]

    results = list(db["events"].aggregate(pipeline))

    cities_collection = db["cities"]

    # Crear un diccionario para almacenar documentos únicos de ciudades
    documents_dict = {}

    for city_data in results:
        city_name = city_data.get("city")
        country = city_data.get("country")
        if city_name and country:
            city_id = generate_city_id(city_name, country)
            documents_dict[city_id] = {
                "_id": city_id,
                "city": city_name,
                "country": country
            }

    documents = list(documents_dict.values())
    print(f"🎯 Total de ciudades únicas detectadas: {len(documents)}")

    # Insertar solo las ciudades nuevas (las que no están en la colección)
    if documents:
        # Evitar insertar ciudades ya existentes
        existing_ids = set(c["_id"] for c in cities_collection.find({}, {"_id": 1}))
        new_documents = [doc for doc in documents if doc["_id"] not in existing_ids]

        if new_documents:
            try:
                cities_collection.insert_many(new_documents, ordered=False)
                print(f"✅ Insertadas {len(new_documents)} ciudades nuevas.")
            except Exception as e:
                print(f"⚠️ Error al insertar nuevas ciudades: {e}")
        else:
            print("ℹ️  Todas las ciudades ya estaban insertadas previamente.")
    else:
        print("ℹ️  No se encontraron ciudades únicas para insertar.")

if __name__ == "__main__":
    collect_unique_cities()