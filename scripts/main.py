from mongodb_connection import save_or_update_event, connect_to_mongodb
from fetch_ticketmaster import fetch_ticketmaster_data
from transform_event import transform_event_data

def main():
    print("📥 Recopilando eventos musicales en España...")
    events = fetch_ticketmaster_data()  # Obtener datos de la API

    if not events:
        print("❌ No se encontraron eventos.")
        return

    print(f"📊 Eventos encontrados: {len(events)}")
    print("🔄 Transformando eventos antes de guardarlos...")

    transformed_events = [transform_event_data(event) for event in events]

    print(f"📁 Guardando {len(transformed_events)} eventos en MongoDB...")

    unchanged_counter = [0]  # Inicializamos el contador

    # Conectar a MongoDB y obtener la colección
    collection = connect_to_mongodb()

    for event in transformed_events:
        save_or_update_event(event, collection, unchanged_counter)  # Ahora pasamos la colección correctamente

    if unchanged_counter[0] > 0:
        print(f"👁️ Eventos sin cambios: {unchanged_counter[0]}")

    print("✅ Proceso finalizado correctamente.")

if __name__ == "__main__":
    main()
