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
    if db is None:
        return

    # Seleccionar la colección "events"
    collection = db[COLLECTION_NAME]
    print(f"📁 Actualizando eventos de la colección {COLLECTION_NAME}")

    # Buscar el evento en la colección usando el ID del evento
    existing_event = collection.find_one({"id": event["id"]})

    if existing_event:  # Si el evento existe en la base de datos
        # Verificar si el estado ha cambiado
        if existing_event.get("status") != event.get("status"):
            # Actualizar el evento si el estado ha cambiado
            collection.update_one({"id": event["id"]}, {"$set": event})
            print(f"🔄 Evento actualizado: {event['name']}")
        else:
            print(f"✅ Evento sin cambios: {event['name']}")  # No actualiza si no hay cambios
    else:
        # Si no existe, insertar el nuevo evento
        collection.insert_one(event)
        print(f"🆕 Nuevo evento guardado: {event['name']}")