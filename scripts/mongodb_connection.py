from pymongo import MongoClient
from config import MONGO_URI

def connect_to_mongodb():
    try:
        # Conectar al cliente de MongoDB usando la URI desde config.py
        client = MongoClient(MONGO_URI)
        # Seleccionar la BBDD "ticketmaster_db"
        db = client["ticketmaster_db"]
        print("✅ Conexión exitosa a MongoDB")
        
        # Obtener la lista de colecciones dentro de esta BBDD
        collections = db.list_collection_names()
        print(f"📁 Colecciones en '{db.name}':", collections)
        
        return db
    
    except Exception as e:
        print(f"❌ Error de conexión: {e}")  # Aquí corregimos el f-string
        return None

def save_events_to_mongodb(events):
    db = connect_to_mongodb()
    if db is not None:
        try:
            collection = db["events"]  # Se asume que la colección se llama 'events'
            # Insertar los eventos en la colección de MongoDB
            result = collection.insert_many(events)
            print(f"✅ {len(result.inserted_ids)} eventos guardados en MongoDB")
            return result.inserted_ids  # Devolver los IDs de los eventos insertados
        except Exception as e:
            print(f"❌ Error al guardar eventos en MongoDB: {e}")
            return None
    else:
        print("❌ No se pudo conectar a la BBDD de MongoDB.")
