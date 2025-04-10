import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src_02 import (
    fetch_ticketmaster_data,
    transform_event_data,
    connect_to_mongodb,
    save_or_update_event,
    update_all_collections,
    update_artist_sentiment,
    generate_fact_events
)

def main():
    # 1. Recopilar eventos desde la API de Ticketmaster
    print("📥 Recopilando eventos musicales en España...")
    events = fetch_ticketmaster_data()  # Obtener datos de la API

    if not events:
        print("❌ No se encontraron eventos.")
        return

    print(f"📊 Eventos encontrados: {len(events)}")
    
    # 2. Transformar coleccion eventos con los campos necesarios
    print("🔄 Transformando eventos antes de guardarlos...")

    transformed_events = [transform_event_data(event) for event in events]

    if not transformed_events:
        print("❌ No hay eventos transformados para guardar.")
        return

    print(f"📁 Guardando {len(transformed_events)} eventos en MongoDB...")

    unchanged_counter = [0]  # Inicializamos el contador

    # 3. Conectar a MongoDB y obtener la colección
    collection = connect_to_mongodb()

    for event in transformed_events:
        save_or_update_event(event, collection, unchanged_counter)  # Ahora pasamos la colección correctamente

    if unchanged_counter[0]:
        print(f"👁️ Eventos sin cambios: {unchanged_counter[0]}")

    print("✅ Proceso finalizado correctamente.")
    
    # 4. Actualizar colecciones derivadas de "events" y guardar en MongoDB
    print("🔄 Actualizando colecciones derivadas desde events...")
    update_all_collections()
    print("✅ Colecciones actualizadas correctamente.")

    # 5. Actualizacion de etiquetas de sentimiento en la colección "artists"
    print("🧠 Iniciando análisis de sentimiento...")
    update_artist_sentiment()
    print("✅ Análisis de sentimiento completado.")
    
    # 5. Generar el dataset normalizado "fact_events" a partir de "events"
    print("📊 Generando tabla de hechos 'fact_events'...")
    generate_fact_events()
    print("✅ Tabla de hechos 'fact_events' actualizada correctamente.")

if __name__ == "__main__":
    main()
