# Transforma los datos de la API de Ticketmaster para almacenarlos en MongoDB de forma estructurada

def transform_event_data(event):
    
    transformed_event = {
        "id": event.get("id"),
        "name": event.get("name"),
        "artist": event.get("_embedded", {}).get("attractions", [{}])[0].get("name"),
        "performers": [
            {"name": artist.get("name")} for artist in event.get("_embedded", {}).get("attractions", [])
        ],
        "event_date": event.get("dates", {}).get("start", {}).get("localDate"),
        "event_time": event.get("dates", {}).get("start", {}).get("localTime"),
        "event_datetime": event.get("dates", {}).get("start", {}).get("dateTime"),
        "segment": event.get("classifications", [{}])[0].get("segment", {}).get("name"),
        "genre": event.get("classifications", [{}])[0].get("genre", {}).get("name"),
        "subgenre": event.get("classifications", [{}])[0].get("subGenre", {}).get("name"),
        "family_friendly": event.get("classifications", [{}])[0].get("family"),
        "event_description": event.get("info") or event.get("pleaseNote"),
        "event_type": event.get("type"),
        "event_image_url": event.get("images", [{}])[1].get("url"),
        "event_tags": [event.get("name") for t in event.get("classifications", [{}])[0].get("subGenre", {}).get("name", [])],
        "start_date": event.get("sales", {}).get("public", {}).get("startDateTime"),
        "end_date": event.get("sales", {}).get("public", {}).get("endDateTime"),
        "organizer": {"name": event.get("promoter", {}).get("name")},
        "ticket_status": event.get("dates", {}).get("status", {}).get("code"),
        "url_compra_entradas": event.get("url"),
        "ticket_types": [
            {
                "type": ticket.get("type"),
                "price": ticket.get("min")  # Precio mínimo
            }
            for ticket in event.get("priceRanges", [])
        ],
        "location": {
            "city": event.get("_embedded", {}).get("venues", {}).get("city"),
            "country": event.get("_embedded", {}).get("venues", {}).get("country"),
            "latitude": event.get("_embedded", {}).get("venues", {}).get("location", {}).get("latitude"),
            "longitude": event.get("_embedded", {}).get("venues", {}).get("location", {}).get("longitude"),
            "postalCode": event.get("_embedded", {}).get("venues", {}).get("postalCode"),
            "address": event.get("_embedded", {}).get("venues", {}).get("address"),
            "place": event.get("_embedded", {}).get("venues", {}).get("name")
        }     
    }
    
    return transformed_event
