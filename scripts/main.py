from fetch_ticketmaster import fetch_ticketmaster_data
from mongodb_connection import save_or_update_event

def main():
    print("📥 Recopilando eventos musicales en España...")
    events = fetch_ticketmaster_data()

    print(f"📊 Eventos encontrados: {len(events)}")  # Verifica que se obtienen eventos
    print(f"📁 ..actualizando la colección en MongoDB, espera unos segundos") # Proceso de actualización con save or update event de MongoDB

    if events:
        unchanged_counter = [0]  # Inicializamos el contador

        for event in events:
            save_or_update_event(event, unchanged_counter)

        if unchanged_counter[0] > 0:
            print(f"👁️ Eventos sin cambios: {unchanged_counter[0]}")
        print("✅ Proceso finalizado correctamente.")
    else:
        print("❌ No se encontraron eventos.")

if __name__ == "__main__":
    main()