import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from pymongo import MongoClient
from config_01 import MONGO_URI, DB_NAME, COLLECTION_NAME
from datetime import datetime
from zoneinfo import ZoneInfo

"""Verifica si el evento de la API es diferente al de la db, excluyendo '_id'."""
def checkEventIsUpdated(event_from_api, event_from_db):
    if not event_from_db:
        return True  # Si el evento no existe en db, considerarlo como actualizado
    
    # Claves que se ignoran al comparar eventos
    IGNORED_KEYS = {"_id", "last_seen"}
    event_from_api_filtered = {key: value for key, value in event_from_api.items() if key not in IGNORED_KEYS}
    event_from_db_filtered = {key: value for key, value in event_from_db.items() if key not in IGNORED_KEYS}
    
    return event_from_api_filtered != event_from_db_filtered

"""Establece conexión con MongoDB y devuelve la colección de eventos."""
def connect_to_mongodb():
    try:
        client = MongoClient(MONGO_URI)  # Conexión al cliente de MongoDB

        db = client[DB_NAME]  # Selección de la base de datos
        
        if COLLECTION_NAME not in db.list_collection_names():
            db.create_collection(COLLECTION_NAME)  # Creación de la colección si no existe
            print(f"📁 Colección '{COLLECTION_NAME}' creada.")

        collection = db[COLLECTION_NAME]  # Selección de la colección

        # Crear un índice único en "id" si no existe
        if "id_1" not in collection.index_information():
            collection.create_index([("id", 1)], unique=True)  # Creación del índice único

        return collection  # Retorno de la colección
    except Exception as e:
        print(f"❌ Error de conexión a MongoDB: {e}")  # Manejo de excepciones
        return None

"""Guarda o actualiza un evento en la base de datos si es nuevo o ha cambiado."""
def save_or_update_event(event, collection, unchanged_counter):
    
    if collection is None:
        print("❌ No se pudo conectar a MongoDB.")
        return

    existing_event = collection.find_one({"id": event["id"]})
    
    # Siempre actualizar la fecha de last_seen al ver el evento en la API
    event["last_seen"] = datetime.now(ZoneInfo("Europe/Madrid")).strftime("%Y-%m-%d")

    if checkEventIsUpdated(event, existing_event):
        collection.update_one({"id": event["id"]}, {"$set": event}, upsert=True)
        status_msg = "🔄 Evento actualizado" if existing_event else "🆕 Evento nuevo"
        print(f"{status_msg}: {event['name']} (Estado: {event.get('ticket_status')})")
    else:
        # Solo actualizar la fecha si el evento no ha cambiado
        collection.update_one({"id": event["id"]}, {"$set": {"last_seen": event["last_seen"]}})
        unchanged_counter[0] += 1

"""Establece conexión con MongoDB y devuelve el objeto de base de datos completo (solo para consultas generales)."""
def connect_to_mongodb_database():
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        return db
    except Exception as e:
        print(f"❌ Error de conexión a MongoDB (database): {e}")
        return None

# Permite la ejecución directa del script para pruebas
if __name__ == "__main__":
    collection = connect_to_mongodb()  # Conexión a MongoDB
    if collection is not None:
        print("✅ Conexión a MongoDB exitosa y colección obtenida.")
    else:
        print("❌ No se pudo establecer conexión con MongoDB.")  # Manejo de error en la conexión
