import os
import sys
# Añade la ruta raíz del proyecto para poder importar módulos correctamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import hashlib
from pymongo import MongoClient
from config_01 import MONGO_URI, DB_NAME

def collect_unique_status():
    # Conexión con la base de datos
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    # Selecciona la colección de eventos y la colección de status
    events_collection = db["events"]
    status_collection = db["status"]

    # Extrae todos los valores distintos del campo 'ticket_status' de los eventos
    all_status_codes = events_collection.distinct("ticket_status")

    # Itera por cada estado distinto encontrado
    for status in all_status_codes:
        if status is None:
            continue  # Omite valores nulos

        # Genera un id único para cada status usando MD5
        status_id = hashlib.md5(status.encode()).hexdigest()
        status_doc = {
            "_id": status_id,
            "status": status
        }

        # Inserta el status si no existe previamente en la colección
        if not status_collection.find_one({"_id": status_id}):
            status_collection.insert_one(status_doc)
            print(f"🆕 Status añadido: {status}")
        else:
            print(f"✅ Status existente: {status}")

if __name__ == "__main__":
    collect_unique_status()
