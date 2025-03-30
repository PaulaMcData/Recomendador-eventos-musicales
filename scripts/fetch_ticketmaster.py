import requests
from config import API_KEY, API_URL

# Petición a la API de Ticketmaster
def fetch_ticketmaster_data():
    try:
        # Parámetros de la solicitud
        params = {
            'apikey': API_KEY,
            'classificationName': 'Music',  # Filtro eventos musicales
            'size': 2  # Número de eventos a obtener
        }

        response = requests.get(API_URL, params=params)

        # Comprobar que la solicitud fue exitosa
        if response.status_code == 200:
            events = response.json()['_embedded']['events']  # Acceder a los eventos
            print(f"✅ Conexión existosa API Ticketmaster {len(events)} eventos musicales encontrados")
            return events
        elif response.status_code == 401:
            print("❌ Error de autenticación: Verifica tu API Key.")
            return []
        else:
            print(f"❌ Error en la solicitud a la API de Ticketmaster. Código de estado: {response.status_code}")
            return []

    except Exception as e:
        print(f"❌ Error en la petición a la API de Ticketmaster: {e}")
        return []