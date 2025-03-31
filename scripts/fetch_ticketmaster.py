import requests
from config import API_KEY, API_URL
from cities import COUNTRY_CODE, SPAIN_CITIES

# Petición a la API de Ticketmaster para obtener eventos musicales en España
def fetch_ticketmaster_data():
    all_events = []  # Lista para almacenar todos los eventos musicales

    for city in SPAIN_CITIES:
        page = 0  # Comenzamos desde la página 0
        while True:
            # Parámetros de la solicitud
            params = {
                'apikey': API_KEY,
                'classificationName': 'Music',  # Filtro eventos musicales
                'countryCode': COUNTRY_CODE,  # Filtro España
                'city': city,  # Ciudad actual dentro del listado de ciudades de España
                'size': 200,  # Máximo eventos por página
                'page': page  # Página actual de los resultados
            }

            response = requests.get(API_URL, params=params)

            # Comprobar que la solicitud fue exitosa
            if response.status_code == 200:
                data = response.json()
                if '_embedded' in data and 'events' in data['_embedded']:
                    events = data['_embedded']['events']

                    # 🔍 Filtrar eventos que contengan "status"
                    filtered_events = [event for event in events if "status" in event]

                    all_events.extend(filtered_events)
                    print(f"✅ {len(filtered_events)} eventos extraídos de {city} (página {page})")

                    if page >= 4:  # Evitamos el límite de 1000 registros
                        break

                    page += 1
                else:
                    break  # No hay más eventos en esta ciudad

            else:
                print(f"⚠️ Error en {city}: {response.status_code}")
                break 
    return all_events
