from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

def checkEventIsUpdated(event_from_api, event_from_db):
    # Usamos un dict sin _id para la comparación
    event_from_api_no_id = {key: value for key, value in event_from_api.items() if key != "_id"}
    event_from_db_no_id = {key: value for key, value in event_from_db.items() if key != "_id"}
    
    return event_from_api_no_id != event_from_db_no_id

def connect_to_mongodb():
    try:

        client = MongoClient(MONGO_URI)

        db = client[DB_NAME]

        # Crear la colección si no existe
        if COLLECTION_NAME not in db.list_collection_names():
            db.create_collection(COLLECTION_NAME)
            print(f"📁 Colección '{COLLECTION_NAME}' creada.")

        collection = db[COLLECTION_NAME]

        # Crear un índice único en "id" (si no existe)
        if "id_1" not in collection.index_information():
            collection.create_index([("id", 1)], unique=True)

        return db
    
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

def save_or_update_event(event, unchanged_counter):

    db = connect_to_mongodb()
    if db is None:
        print("❌ No se pudo conectar a MongoDB.")
        return
    
    collection = db[COLLECTION_NAME]
    
    # Asegurar que la colección existe antes de buscar
    if COLLECTION_NAME not in db.list_collection_names():
        print(f"⚠️ La colección '{COLLECTION_NAME}' no existe, se creará al insertar el primer evento.")

    # Buscar si el evento ya existe en la BD
    existing_event = collection.find_one({"id": event["id"]})
    existing_status_code = existing_event.get("dates", {}).get("status", {}).get("code") if existing_event else None
    new_status_code = event.get("dates", {}).get("status", {}).get("code")
    isUpdated = checkEventIsUpdated(event, existing_event)

    if existing_event:
        # Comparar todos los datos del evento, no solo el status.code
        if isUpdated:
            collection.update_one({"id": event["id"]}, {"$set": event})
            print(f"🔄 Evento actualizado: {event['name']} (Estado: {existing_status_code} → {new_status_code})")
        else:
            unchanged_counter[0] += 1 # No cambia el estado del evento
            
    else:

        collection.insert_one(event)
        print(f"🆕 Evento nuevo: {event['name']} (Estado: {new_status_code})")
