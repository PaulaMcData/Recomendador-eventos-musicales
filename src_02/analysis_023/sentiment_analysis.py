import os
import sys
import requests
import json
import unicodedata
from dotenv import load_dotenv
from textblob import TextBlob
from src_02.database_022.mongodb_connection import connect_to_mongodb_database

# Cargar variables de entorno
load_dotenv()
API_KEY = os.getenv("API_KEY_LASTFM").strip('"')

# Funciones auxiliares
def normalizar_para_comparar(texto):
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    return texto.lower().replace(" ", "").replace("'", "").replace("&", "and")

def get_artist_tags(artist_name):
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "artist.getTopTags",
        "artist": artist_name,
        "api_key": API_KEY,
        "format": "json"
    }
    response = requests.get(url, params=params)
    return response.json()

def extraer_tags_como_texto(tags_json, top_n=10, excluir_comunes=True):
    try:
        tags = tags_json.get('toptags', {}).get('tag', [])
        artist_name_raw = tags_json.get('toptags', {}).get('@attr', {}).get('artist', '')
        artist_name_clean = normalizar_para_comparar(artist_name_raw)
        comunes = {"seen live", "favorites", "00s", "90s", "80s", "70s", "british", "beautiful", "best"}
        tag_names = []
        for tag in tags[:top_n]:
            name = tag.get("name", "").strip()
            if not name:
                continue
            name_lower = name.lower()
            if excluir_comunes and name_lower in comunes:
                continue
            if artist_name_clean in normalizar_para_comparar(name):
                continue
            tag_names.append(name)
        return " ".join(tag_names).strip()
    except Exception as e:
        print("  Error al procesar los tags:", e)
        return ""

def analizar_sentimiento(texto):
    if texto:
        blob = TextBlob(texto)
        polaridad = blob.sentiment.polarity
        if polaridad > 0.2:
            interpretacion = "Positivo"
        elif polaridad < -0.2:
            interpretacion = "Negativo"
        else:
            interpretacion = "Neutro"
        return polaridad, interpretacion
    else:
        return 0.0, "Sin texto para analizar"

def guardar_sentimiento_en_mongo(artists_collection, artist_name, sentiment_text, polarity_value):
    nombre_normalizado = normalizar_para_comparar(artist_name)
    for artista in artists_collection.find():
        nombre_en_mongo = artista.get("artist", "")
        if normalizar_para_comparar(nombre_en_mongo) == nombre_normalizado:
            artists_collection.update_one(
                {"_id": artista["_id"]},
                {"$set": {
                    "sentiment": sentiment_text,
                    "polarity": polarity_value
                }}
            )
            print(f"  Sentimiento guardado correctamente para '{nombre_en_mongo}'")
            return
    print(f"  No se encontró el artista '{artist_name}' (ni siquiera normalizado)")

def update_artist_sentiment():
    db = connect_to_mongodb_database()
    artists_collection = db["artists"]
    total_artistas = 0
    procesados_ok = 0
    sin_etiquetas = 0
    for artista in artists_collection.find():
        nombre_original = artista.get("artist", "")
        if not nombre_original:
            continue
        total_artistas += 1
        try:
            tags_json = get_artist_tags(nombre_original)
            texto_tags = extraer_tags_como_texto(tags_json)
            if not texto_tags:
                sin_etiquetas += 1
                continue
            polaridad, sentimiento = analizar_sentimiento(texto_tags)
            guardar_sentimiento_en_mongo(artists_collection, nombre_original, sentimiento, polaridad)
            procesados_ok += 1
        except Exception as e:
            print(f"  Error con artista '{nombre_original}':", e)
            sin_etiquetas += 1
    print(f"\n✅ Sentimiento actualizado para {procesados_ok} artistas.")
    print(f"❌ No se pudieron analizar {sin_etiquetas} artistas.")
    print(f"🎵 Total procesados: {total_artistas}")
