from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

# Conexión a MongoDB
client = MongoClient(MONGO_URI)
db = client["eventos_db"]
artists_collection = db["artists"]

# Insertar un artista (puedes hacerlo dinámicamente según los datos)
def insert_artist(name):
    artist_data = {
        "name": name
    }

    artist_id = artists_collection.insert_one(artist_data).inserted_id
    return artist_id
