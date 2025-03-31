from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

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

    # Extraer el status.code del nuevo evento
    new_status_code = event.get("dates", {}).get("status", {}).get("code")

    if existing_event:
        # Extraer el status.code del evento existente
        existing_status_code = existing_event.get("dates", {}).get("status", {}).get("code")

        if existing_status_code != new_status_code:
            collection.update_one({"id": event["id"]}, {"$set": event})
            print(f"🔄 Evento actualizado: {event['name']} (Estado: {existing_status_code} → {new_status_code})")
        else:
            unchanged_counter[0] += 1  # Contador de eventos sin cambios
            print(f"✅ Evento sin cambios: {unchanged_counter}")
    else:

        collection.insert_one(event)
        print(f"🆕 Evento nuevo: {event['name']} (Estado: {new_status_code})")
