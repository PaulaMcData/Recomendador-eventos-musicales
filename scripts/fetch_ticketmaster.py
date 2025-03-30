import requests
from config import API_KEY, API_URL

# Petición a la API de Ticketmaster para obtener todos los eventos musicales
def fetch_ticketmaster_data():
    all_events = []  # Lista para almacenar todos los eventos musicales
    page = 0  # Comenzamos desde la página 0
    while True:
        try:
            # Parámetros de la solicitud
            params = {
                'apikey': API_KEY,
                'classificationName': 'Music',  # Filtro eventos musicales
                'size': 200,  # Número máximo de eventos por página (200 es el límite de Ticketmaster)
                'page': page  # Página actual de los resultados
            }

            response = requests.get(API_URL, params=params)

            # Comprobar que la solicitud fue exitosa
            if response.status_code == 200:
                events = response.json().get('_embedded', {}).get('events', [])  # Acceder a los eventos

                if not events:  # Si no hay más eventos, terminamos
                    break

                print(f"✅ Página {page + 1} - {len(events)} eventos musicales encontrados")
                all_events.extend(events)  # Añadir los eventos actuales a la lista

                page += 1  # Incrementar la página para la siguiente solicitud

            elif response.status_code == 401:
                print("❌ Error de autenticación: Verifica tu API Key.")
                break
            else:
                print(f"❌ Error en la solicitud a la API de Ticketmaster. Código de estado: {response.status_code}")
                break

        except Exception as e:
            print(f"❌ Error en la petición a la API de Ticketmaster: {e}")
            break

    print(f"✅ Se han encontrado un total de {len(all_events)} eventos musicales.")
    return all_events