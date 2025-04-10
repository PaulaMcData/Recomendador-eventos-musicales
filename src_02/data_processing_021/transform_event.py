import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Transformacion de los datos obtenidos de la API Ticketmaster
def transform_event_data(event):
    venue = event.get("_embedded", {}).get("venues", [{}])
    venue = venue[0] if venue else {}

    transformed_event = {
        "id": event.get("id"),
        "name": event.get("name"),
        "artist": event.get("_embedded", {}).get("attractions", [{}])[0].get("name", None),
        "event_datetime": event.get("dates", {}).get("start", {}).get("dateTime"),
        "segment": event.get("classifications", [{}])[0].get("segment", {}).get("name"),
        "genre": event.get("classifications", [{}])[0].get("genre", {}).get("name"),
        "subgenre": event.get("classifications", [{}])[0].get("subGenre", {}).get("name"),
        "family_friendly": event.get("classifications", [{}])[0].get("family"),
        "event_type": event.get("type"),
        "event_image_url": event.get("images", [{}])[0].get("url", None),
        "start_date": event.get("sales", {}).get("public", {}).get("startDateTime"),
        "end_date": event.get("sales", {}).get("public", {}).get("endDateTime"),
        "organizer": event.get("promoter", {}).get("name", None),
        "ticket_status": event.get("dates", {}).get("status", {}).get("code"),
        "url_compra_entradas": event.get("url"),
        "location": {
            "city": venue.get("city", None).get("name"),
            "country": venue.get("country", None).get("name"),
            "latitude": venue.get("location", {}).get("latitude"),
            "longitude": venue.get("location", {}).get("longitude"),
            "postalCode": venue.get("postalCode"),
            "address": venue.get("address", {}).get("line1"),
            "place": venue.get("name")
        },
        "ticket_types": [
            {
                "type": ticket.get("type", "Standard"),
                "currency": ticket.get("currency"),
                "min_price": ticket.get("min"),
                "max_price": ticket.get("max")
            }
            for ticket in event.get("priceRanges") or []
        ]
    }
    
    return transformed_event
