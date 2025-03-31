from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

def checkEventIsUpdated(event_from_api, event_from_db):
    """Verifica si el evento de la API es diferente al de la db, excluyendo '_id'."""
    if not event_from_db:
        return True  # Si el evento no existe en BD, considerarlo como actualizado
    
    event_from_api_no_id = {key: value for key, value in event_from_api.items() if key != "_id"}
    event_from_db_no_id = {key: value for key, value in event_from_db.items() if key != "_id"}
    
    return event_from_api_no_id != event_from_db_no_id

def connect_to_mongodb():
    """Establece conexión con MongoDB y devuelve la colección de eventos."""
    try:

        client = MongoClient(MONGO_URI)

        db = client[DB_NAME]
        
        if COLLECTION_NAME not in db.list_collection_names():
            db.create_collection(COLLECTION_NAME)
            print(f"📁 Colección '{COLLECTION_NAME}' creada.")

        collection = db[COLLECTION_NAME]

        # Crear un índice único en "id" si no existe
        if "id_1" not in collection.index_information():
            collection.create_index([("id", 1)], unique=True)

        return collection
    except Exception as e:
        print(f"❌ Error de conexión a MongoDB: {e}")
        return None

def save_or_update_event(event, collection, unchanged_counter):
    """Guarda o actualiza un evento en la base de datos si es nuevo o ha cambiado."""
    if collection is None:
        print("❌ No se pudo conectar a MongoDB.")
        return

    existing_event = collection.find_one({"id": event["id"]})
    
    if checkEventIsUpdated(event, existing_event):
        collection.update_one({"id": event["id"]}, {"$set": event}, upsert=True)
        status_msg = "🔄 Evento actualizado" if existing_event else "🆕 Evento nuevo"
        print(f"{status_msg}: {event['name']} (Estado: {event.get('dates', {}).get('status', {}).get('code')})")
    else:
        unchanged_counter[0] += 1  # Incrementar contador de eventos sin cambios
