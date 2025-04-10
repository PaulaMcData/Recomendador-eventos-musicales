from datetime import datetime

def formatear_hora(hora_str):
    if hora_str and ":" in hora_str:
        return ":".join(hora_str.split(":")[:2])
    return "No disponible"

def formatear_fecha_hora_zulu(zulu_str, fecha_primero=True):
    try:
        dt_obj = datetime.strptime(zulu_str, "%Y-%m-%dT%H:%M:%SZ")
        if fecha_primero:
            return f"{dt_obj.strftime('%Y-%m-%d')} ⏰ Hora: {dt_obj.strftime('%H:%M')}"
        else:
            return f"{dt_obj.strftime('%d-%m-%Y')} ⏰ Hora: {dt_obj.strftime('%H:%M')}"
    except:
        return zulu_str

def formatear_evento(event, artist_name, city_name, genre_name, subgenre_name, status_name, organizer_name, sentiment):
    hora_evento = formatear_hora(event.get('event_time', 'No disponible'))
    start_formatted = formatear_fecha_hora_zulu(event.get('start_date'), fecha_primero=False) if event.get('start_date') else "No disponible"
    end_formatted = formatear_fecha_hora_zulu(event.get('end_date'), fecha_primero=False) if event.get('end_date') else "No disponible"
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
📅 Fecha: {event.get('event_date', 'No disponible')} ⏰ Hora: {hora_evento}
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
