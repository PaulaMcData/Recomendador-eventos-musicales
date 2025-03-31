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
        "genre": event.get("classifications", [{}])[0].get("genre", {}).get("name"),
        "subgenre": event.get("classifications", [{}])[0].get("subGenre", {}).get("name"),
        "is_family_friendly": event.get("classifications", [{}])[0].get("family"),
        "event_description": event.get("info") or event.get("pleaseNote"),
        "event_type": event.get("type"),
        "event_image_url": event.get("images", [{}])[0].get("url"),
        "event_tags": [event.get("name") for t in event.get("classifications", [{}])[0].get("subGenre", {}).get("name", [])],
        "start_date": event.get("dates", {}).get("start", {}).get("localDate"),
        "end_date": event.get("dates", {}).get("end", {}).get("localDate"),
        "organizer": {"name": event.get("promoter", {}).get("name")},
        "ticket_available": event.get("dates", {}).get("status", {}).get("code"),
        "url_compra_entradas": event.get("url"),
        "dates": {
            "status": {
                "code": event.get("dates", {}).get("status", {}).get("code")
            }
        },
        "ticket_types": [
            {
                "type": ticket.get("type"),
                "price": ticket.get("min")  # Precio mínimo
            }
            for ticket in event.get("priceRanges", [])
        ],
        "currency": event.get("priceRanges", [{}])[0].get("currency"),
        "location": {
            "city": event.get("place", {}).get("city", {}).get("name"),
            "country": event.get("place", {}).get("country", {}).get("name"),
            "latitude": event.get("place", {}).get("location", {}).get("latitude"),
            "longitude": event.get("place", {}).get("location", {}).get("longitude"),
            "address": event.get("place", {}).get("address", {}).get("line1"),
            "venue": event.get("_embedded", {}).get("venues", [{}])[0].get("name")
        }     
    }
    
    return transformed_event
