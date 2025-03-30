from fetch_ticketmaster import fetch_ticketmaster_data
from mongodb_connection import save_events_to_mongodb

# Test de conexión y funcionamiento de la API de Ticketmaster y MongoDB
def test_fetch_and_save():
    print("🔄 Iniciando la prueba de fetch y guardado de datos...")
    events = fetch_ticketmaster_data()
    if events:
        save_events_to_mongodb(events)
    else:
        print("❌ No se encontraron eventos musicales o hubo un error en la API.")

if __name__ == "__main__":
    test_fetch_and_save()