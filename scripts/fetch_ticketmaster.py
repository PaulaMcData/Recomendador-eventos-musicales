import requests
from config import API_KEY, API_URL
from cities import COUNTRY_CODE, SPAIN_CITIES

MAX_RETRIES = 3  # Intentos máximos en caso de fallo
PAGE_LIMIT = 4   # Límite de páginas para evitar 1000+ registros

def fetch_city_events(city):
    """Obtiene eventos musicales de una ciudad específica desde la API de Ticketmaster."""
    all_events = []
    page = 0 

    while page <= PAGE_LIMIT:
        params = {
            'apikey': API_KEY,
            'classificationName': 'Music',  # Filtro eventos musicales
            'countryCode': COUNTRY_CODE,    # Filtro España
            'city': city,                   # Ciudad actual
            'size': 200,                     # Máx. eventos por página
            'page': page                     # Página actual
        }

        retries = 0
        while retries < MAX_RETRIES:
            try:
                response = requests.get(API_URL, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if '_embedded' in data and 'events' in data['_embedded']:
                        events = data['_embedded']['events']
                        filtered_events = [event for event in events if event.get("dates", {}).get("status", {}).get("code")]
                        all_events.extend(filtered_events)
                        print(f"🔍 {len(filtered_events)} eventos en {city} (pág.{page})")

                        # Si el número de eventos es menor que el tamaño de página, ya no hay más eventos
                        if len(events) < 200:
                            return all_events

                        page += 1        
                    else:
                        return all_events  # No más eventos en esta ciudad
                else:
                    print(f"⚠️ Error {response.status_code} en {city}. Reintentando...")
                    retries += 1

            except requests.exceptions.RequestException as e:
                print(f"⏳ Error de conexión en {city}: {e}. Reintentando...")
                retries += 1

        if retries >= MAX_RETRIES:
            print(f"❌ No se pudo obtener eventos en {city} tras varios intentos.")
            return all_events

    return all_events


def fetch_ticketmaster_data():
    """Obtiene eventos musicales de todas las ciudades en España."""
    all_events = []
    for city in SPAIN_CITIES:
        city_events = fetch_city_events(city)
        all_events.extend(city_events)
    
    print(f"🎵 Total eventos recopilados: {len(all_events)}")
    return all_events
