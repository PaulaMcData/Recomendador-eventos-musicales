### Test connection VS y MongoDB ###

from pymongo import MongoClient # type: ignore

# Sustituir con mi cadena de conexion
connection_string = "mongodb+srv://paulamcdata:Gp2025.@clustergp-eventos.c1syxjt.mongodb.net/?retryWrites=true&w=majority&appName=ClusterGP-Eventos"

try:
    # Conectar al cliente de MongoDB
    client = MongoClient(connection_string)
    # Obtener la lista de base de datos disponibles
    dbs= client.list_database_names()

    print("✅ Conexión exitosa a MongoDB Atlas")
    print("📂 Bases de datos disponibles:", dbs)

except Exception as e:
    print("❌ Error de conexión:", e)