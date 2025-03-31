from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

def connect_to_mongodb():
    try:
        # Conectar al cliente de MongoDB usando la URI desde config.py
        client = MongoClient(MONGO_URI)
        # Seleccionar la BBDD "ticketmaster_db"
        db = client[DB_NAME]
        print("✅ Conexión exitosa a MongoDB")

        return db
    
    except Exception as e:
        print(f"❌ Error de conexión: {e}")  # Aquí corregimos el f-string
        return None

def save_or_update_event(event):
    # LLamamos a la función anterior para conectar con MongoDB
    db = connect_to_mongodb()
    # Seleccionar la colección "events"
    collection = db[COLLECTION_NAME]
    print(f"📁 Actualizando eventos de la colección {collection}")

    existing_event = collection.find_one({"id": event["id"]})

    # Actualizar eventos si el status ha cambiado y si es nuevo se guarda en la base de datos
    if existing_event: # Si el evento existe
        if existing_event["status"] != event["status"]:
            collection.update_one({"id": event["id"]}, {"$set": event}) # Actualiza si cambia de estado
            print(f"🔄 Evento actualizado: {event['name']}")
        else:
            print(f"✅ Evento sin cambios: {event['name']}") # No actualiza si no cambia de estado
    else:
        collection.insert_one(event) # Inserta un evento nuevo (si no lo encuentra) y lo guarda
        print(f"🆕 Nuevo evento guardado: {event['name']}") 