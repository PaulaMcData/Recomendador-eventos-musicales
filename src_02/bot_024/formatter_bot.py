from datetime import datetime

def formatear_fecha_hora_zulu(zulu_str):
    formatos_entrada = [
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%fZ"
    ]
    for fmt in formatos_entrada:
        try:
            dt_obj = datetime.strptime(zulu_str, fmt)
            return dt_obj.strftime("%d-%m-%Y ⏰ Hora: %H:%M")
        except ValueError:
            continue
    return zulu_str

def formatear_evento(event, artist_name, city_name, genre_name, subgenre_name, status_name, organizer_name, sentiment):
    fecha_evento = formatear_fecha_hora_zulu(event.get('event_datetime')) if event.get('event_datetime') else "No disponible"
    start_formatted = formatear_fecha_hora_zulu(event.get('start_date')) if event.get('start_date') else "No disponible"
    end_formatted = formatear_fecha_hora_zulu(event.get('end_date')) if event.get('end_date') else "No disponible"
    familiar = event.get('event_family_friendly')
    familiar_str = "Sí, es un evento familiar" if familiar else "No, no es un evento familiar"

    # Diccionario para asignar iconos según el sentimiento
    SENTIMENT_ICONS = {
        "Positivo": "😊",
        "Neutro": "😐",
        "Negativo": "😞"
    }

    SENTIMENT_NORMALIZED = {
        "Positivo": "positiva",
        "Neutro": "neutra",
        "Negativo": "negativa"
    }
    sentiment_icon = SENTIMENT_ICONS.get(sentiment, "❓")  # Icono por defecto si el sentimiento no es válido
    sentiment_normalized = SENTIMENT_NORMALIZED.get(sentiment, None)

    texto = f"""
🎵 Evento: {event.get('event_name', 'No disponible')}
🎤 Artista: {artist_name}
🏙️ Ciudad: {city_name}
📅 Fecha: {fecha_evento}
🎼 Segmento: {event.get('segment', 'No disponible')}
🎵 Género: {genre_name}
🎶 Subgénero: {subgenre_name}
🎟️ Estado entradas: {status_name}
🕒 Venta desde: {start_formatted}
🚫 Venta hasta: {end_formatted}
📢 Organizador: {organizer_name}
👨‍👩‍👧‍👦 Familiar: {familiar_str}
🔗 Comprar entradas: {event.get('url_compra_entradas', 'No disponible')}
""".strip()
    
    if sentiment:
            # Añadir el campo "Opinión" al mensaje final
            texto += f"\n📝 Opinión: {artist_name} tiene una percepción general {sentiment_normalized} {sentiment_icon} entre los fans de Last.fm."

    
    return texto
