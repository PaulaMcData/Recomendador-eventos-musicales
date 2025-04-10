import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Permite que el script funcione correctamente como parte del paquete (desde main.py o con -m)
from .collect_artists import collect_unique_artists
from .collect_genres import collect_unique_genres
from .collect_status import collect_unique_status
from .collect_places import collect_unique_places
from .collect_cities import collect_unique_cities
from .collect_organizer import collect_unique_organizers

def update_all_collections():
    try:
        print("🎸 Recogiendo artistas...")
        collect_unique_artists()

        print("🎼 Recogiendo géneros musicales...")
        collect_unique_genres()

        print("📋 Recogiendo estados...")
        collect_unique_status()

        print("📍 Recogiendo lugares...")
        collect_unique_places()

        print("🏙️ Recogiendo ciudades...")
        collect_unique_cities()

        print("🎟️ Recogiendo organizadores...")
        collect_unique_organizers()

        print("✅ Todas las colecciones se han actualizado correctamente.")

    except Exception as e:
        print("❌ Error durante la actualización de colecciones:")
        print(e)

if __name__ == "__main__":
    update_all_collections()
