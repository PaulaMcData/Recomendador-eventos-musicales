from pymongo import MongoClient
from config import MONGO_URI

try:
    # Conectar al cliente de MongoDB
    client = MongoClient(MONGO_URI)

    # Obtener la lista de BBDD disponibles
    dbs = client.list_database_names()
    print("✅ Conexión exitosa a MongoDB Atlas")
    print("📂 BBDD disponibles:", dbs)

    # Seleccionar la BBDD "ticketmaster_db"
    db = client["ticketmaster_db"]

    # Obtener la lista de colecciones dentro de esta BBDD
    collections = db.list_collection_names()
    print(f"📁 Colecciones en '{db.name}':", collections)

except Exception as e:
    print("❌ Error de conexión:", e)
    