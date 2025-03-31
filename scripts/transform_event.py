# Transforma los datos de la API de Ticketmaster para almacenarlos en MongoDB de forma estructurada

def transform_event_data(event):
    
    transformed_event = {
        "id": event.get("id"),
        "name": event.get("name"),
        "artist": event.get("_embedded", {}).get("attractions", [{}])[0].get("name"),
        "event_date": event.get("dates", {}).get("start", {}).get("localDate"),
        "event_time": event.get("dates", {}).get("start", {}).get("localTime"),
        "event_datetime": event.get("dates", {}).get("start", {}).get("dateTime"),
        "segment": event.get("classifications", [{}])[0].get("segment", {}).get("name"),
        "genre": event.get("classifications", [{}])[0].get("genre", {}).get("name"),
        "subgenre": event.get("classifications", [{}])[0].get("subGenre", {}).get("name"),
        "family_friendly": event.get("classifications", [{}])[0].get("family"),
        "event_type": event.get("type"),
        "event_image_url": event.get("images", [{}])[1].get("url"),
        "start_date": event.get("sales", {}).get("public", {}).get("startDateTime"),
        "end_date": event.get("sales", {}).get("public", {}).get("endDateTime"),
        "organizer": event.get("promoter", {}).get("name"),
        "ticket_status": event.get("dates", {}).get("status", {}).get("code"),
        "url_compra_entradas": event.get("url"),
        "location": {
            "city": event.get("_embedded", {}).get("venues", [{}])[0].get("city", {}).get("name"),
            "country": event.get("_embedded", {}).get("venues", [{}])[0].get("country", {}).get("name"),
            "latitude": event.get("_embedded", {}).get("venues", [{}])[0].get("location", {}).get("latitude"),
            "longitude": event.get("_embedded", {}).get("venues", [{}])[0].get("location", {}).get("longitude"),
            "postalCode": event.get("_embedded", {}).get("venues", [{}])[0].get("postalCode"),
            "address": event.get("_embedded", {}).get("venues", [{}])[0].get("address", {}).get("line1"),
            "place": event.get("_embedded", {}).get("venues", [{}])[0].get("name")
        }     
    }
    
    return transformed_event
