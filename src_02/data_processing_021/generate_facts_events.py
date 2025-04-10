import sys
import os
import unicodedata
# Añade la ruta raíz del proyecto para poder importar módulos correctamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from pymongo import MongoClient
import hashlib
from config_01 import MONGO_URI, DB_NAME

# Función principal que transforma y normaliza los eventos de la colección 'events'
def generate_fact_events():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    events_collection = db["events"]
    fact_events_collection = db["fact_events"]

    fact_documents = []

    for event in events_collection.find():
        event_id = event.get("id")
        name = event.get("name")
        date = event.get("event_date")
        artist_name = event.get("artist")
        genre_name = event.get("genre")
        subgenre_name = event.get("subgenre")
        status_name = event.get("ticket_status")
        location = event.get("location", {})
        city_name = location.get("city")
        city_country = location.get("country")
        place_name = location.get("place")

        if not all([artist_name, genre_name, status_name, city_name, place_name]):
            continue  # Saltar si falta algún campo clave

        # Normaliza un texto eliminando tildes, convirtiendo a minúsculas y quitando espacios
        def normalize(text):
            if not text:
                return ""
            text = text.strip().lower()
            text = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("utf-8")
            return text

        artist_id = hashlib.md5(normalize(artist_name).encode("utf-8")).hexdigest()
        genre_id = hashlib.md5(f"{normalize(genre_name)}_{normalize(subgenre_name)}".encode("utf-8")).hexdigest() if genre_name and subgenre_name else None
        status_id = hashlib.md5(normalize(status_name).encode("utf-8")).hexdigest()
        city_id = hashlib.md5(f"{normalize(city_name)}_{normalize(city_country)}".encode("utf-8")).hexdigest() if city_name and city_country else None
        place_id = hashlib.md5(f"{normalize(place_name)}_{normalize(city_name)}".encode("utf-8")).hexdigest()
        organizer_name = event.get("organizer", None)
        organizer_id = hashlib.md5(normalize(organizer_name).encode("utf-8")).hexdigest() if organizer_name else None

        doc = {
            "_id": event_id,
            "event_name": name if name else None,
            "artist_id": artist_id,
            "event_date": date,
            "event_time": event.get("event_time"),
            "event_datetime": event.get("event_datetime"),
            "segment": event.get("segment"),
            "genre_id": genre_id,
            "event_family_friendly": event.get("family_friendly"),
            "event_type": event.get("event_type"),
            "event_image_url": event.get("event_image_url"),
            "start_date": event.get("start_date"),
            "end_date": event.get("end_date"),
            "organizer_id": organizer_id,
            "status_id": status_id,
            "url_compra_entradas": event.get("url_compra_entradas"),
            "city_id": city_id,
            "place_id": place_id,
            "ticket_types": event.get("ticket_types", []),
            "event_last_seen": event.get("last_seen")
        }
        fact_documents.append(doc)

    if fact_documents:
        fact_events_collection.delete_many({})  # Limpiar colección anterior
        fact_events_collection.insert_many(fact_documents)
        print(f"📦 'fact_events' creado con {len(fact_documents)} registros.")
    else:
        print("ℹ️ No se generaron registros para 'fact_events'.")

if __name__ == "__main__":
    generate_fact_events()
