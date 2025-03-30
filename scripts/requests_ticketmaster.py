import requests

# Reemplaza esto con tu Consumer Key de Ticketmaster
api_key = "EcNBsXOPdNLFS6vCKYefRzlmzMyyejkB"

# URL de la API de Ticketmaster (puedes agregar más parámetros según sea necesario)
url = f"https://app.ticketmaster.com/discovery/v2/events.json?apikey={api_key}"

# Realiza la petición GET
response = requests.get(url)

# Verifica si la petición fue exitosa
if response.status_code == 200:
    data = response.json()  # Convierte la respuesta JSON en un diccionario de Python
    print(data)
else:
    print(f"Error al hacer la petición: {response.status_code}")