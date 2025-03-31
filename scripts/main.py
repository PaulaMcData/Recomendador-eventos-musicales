from fetch_ticketmaster import fetch_ticketmaster_data
from mongodb_connection import save_or_update_event

def main():
    print("🔄 Iniciando la recopilación de eventos musicales en España...")
    events = fetch_ticketmaster_data()

    if events:
        for event in events:
            save_or_update_event(event)
        print("✅ Proceso finalizado correctamente.")
    else:
        print("❌ No se encontraron eventos.")

if __name__ == "__main__":
    main()