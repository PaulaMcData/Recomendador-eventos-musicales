import sys
import os
from hashlib import md5
from functools import partial 
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import asyncio
import logging
import unicodedata
from aiohttp import web
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from config_01 import TELEGRAM_BOT_TOKEN, RENDER_URI
from src_02.database_022.mongodb_connection import connect_to_mongodb_database
from formatter_bot import formatear_evento

# Configuración del logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Conexión a MongoDB
db = connect_to_mongodb_database()

user_last_command = {}  # Almacena el último comando enviado por cada usuario
user_message_states = {}

GENRE_TRANSLATIONS = {
    "clasica": "classical",
    "alternativa": "alternative",
    "pop": "pop",
    "jazz": "jazz",
    "electronica": "electronic",
    "hip hop": "hip-hop/rap",
    "metal": "metal",
    "blues": "blues",
    # Agrega más géneros según sea necesario
}

async def set_webhook(app):
    webhook_url = RENDER_URI
    await app.bot.set_webhook(url=webhook_url)

# Tu función de manejador del webhook
async def webhook_handler(request, app):
    try:
        update = Update.de_json(await request.json(), app.bot)
        await app.process_update(update)
    except Exception as e:
        logging.exception("❌ Error procesando la actualización del webhook")
    return web.Response()

async def main():
    try:
        # Inicializa la aplicación del bot
        app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
        await app.initialize()  # Inicializa la aplicación explícitamente
        app.add_handler(CommandHandler("hola", hola_command))
        app.add_handler(CommandHandler("ayuda", ayuda_command))
        app.add_handler(CommandHandler("stop", stop_command))
        app.add_handler(CommandHandler("ciudad", ciudad_command))
        app.add_handler(CommandHandler("artista", artista_command))
        app.add_handler(CommandHandler("genero", genero_command))

        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        # Configura el webhook de forma asincrónica
        await set_webhook(app)

        # Configuración del servidor aiohttp
        aiohttp_app = web.Application()
        aiohttp_app.router.add_post("/telegram-webhook", partial(webhook_handler, app=app))

        print("🤖 Bot de Telegram iniciado con webhook. Esperando mensajes...")
        
        # Inicia el servidor aiohttp usando el bucle de eventos existente
        runner = web.AppRunner(aiohttp_app)
        await runner.setup()
        site = web.TCPSite(runner, host="0.0.0.0", port=10000)
        await site.start()

        # Mantén el servidor corriendo
        while True:
            await asyncio.sleep(3600)

    except Exception as e:
        logging.exception("❌ Error al iniciar el bot")
        print("❌ No se pudo iniciar el bot. Revisa la configuración.")

def normalizar_texto(texto):
    texto = texto.strip().lower()
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')
    return texto

def traducir_genero(genero_es):
    """Traduce un género en español al inglés usando el diccionario GENRE_TRANSLATIONS."""
    genero_norm = normalizar_texto(genero_es)
    return GENRE_TRANSLATIONS.get(genero_norm, None)  # Devuelve None si no se encuentra

def generar_city_id(city, country="Spain"):
    texto = f"{normalizar_texto(city)}{normalizar_texto(country)}"
    return md5(texto.encode('utf-8')).hexdigest()

def obtener_datos_evento(event):
    """Extrae y devuelve los campos de texto del evento desde otras colecciones."""
    artist_doc = db["artists"].find_one({"_id": event.get("artist_id")})
    city_doc = db["cities"].find_one({"_id": event.get("city_id")})
    genre_doc = db["genres"].find_one({"_id": event.get("genre_id")})
    status_doc = db["status"].find_one({"_id": event.get("status_id")})
    organizer_doc = db["organizers"].find_one({"_id": event.get("organizer_id")})

    return {
        "artist_name": artist_doc["artist"] if artist_doc else "No disponible",
        "city_name": city_doc["city"] if city_doc else "No disponible",
        "genre_name": genre_doc["genre"] if genre_doc else "No disponible",
        "subgenre_name": genre_doc.get("subgenre", "No disponible") if genre_doc else "No disponible",
        "status_name": status_doc["status"] if status_doc else "No disponible",
        "organizer_name": organizer_doc["organizer"] if organizer_doc else "No disponible",
        "sentiment": artist_doc.get("sentiment", "Sin opinión") if artist_doc else "Sin opinión"

    }

async def hola_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "¡Hola! 👋 Soy tu recomendador de eventos musicales en España 🇪🇸🎶.\n"
        "Escríbeme el nombre de tu ciudad o artista favorito y te ayudaré a descubrir conciertos y festivales."
    )

async def ayuda_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Puedes escribirme el nombre de una ciudad o un artista y te recomendaré eventos musicales.\n"
        "También puedes usar el comando /hola para comenzar de nuevo."
    )

async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando para detener el envío de mensajes."""
    user_id = update.message.chat_id
    user_message_states[user_id] = False  # Cambia el estado a False para detener el envío
    await update.message.reply_text("🚫 Envío de mensajes detenido. Si deseas continuar, envíame otra consulta.")

async def ciudad_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.chat_id
    user_last_command[user_id] = "ciudad"  # Actualiza el estado del usuario
    user_message_states[user_id] = True 
    await update.message.reply_text(
        "🏙️ ¡Vamos allá! ¿Sobre qué ciudad española quieres descubrir conciertos o festivales? 🎶\n"
        "Escríbeme la ciudad y buscaré los mejores eventos para ti. 🎉"
    )

async def artista_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.chat_id
    user_last_command[user_id] = "artista"  # Actualiza el estado del usuario
    user_message_states[user_id] = True 
    await update.message.reply_text(
        "🎤 ¡Genial! ¿Quién es tu artista favorito? 😍\n"
        "Escríbeme su nombre y te diré si tiene eventos en España. 🎫🇪🇸"
    )

async def genero_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.chat_id
    user_last_command[user_id] = "genero"  # Actualiza el estado del usuario
    user_message_states[user_id] = True 
    await update.message.reply_text(
        "🎼 ¡Genial! ¿Qué género musical te interesa? 🎶\n"
        "Escríbeme el nombre del género (por ejemplo, Rock, Pop, Jazz) y buscaré eventos relacionados. 🎤"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if db is None:
            logging.error("❌ No se pudo conectar a MongoDB.")
            await update.message.reply_text("❌ Error de conexión con la base de datos.")
            return

        user_input = update.message.text
        user_input_norm = normalizar_texto(user_input)
        user_id = update.message.chat_id

        # Verifica el último comando del usuario
        last_command = user_last_command.get(user_id)

        events_collection = db["fact_events"]
        artists_collection = db["artists"]
        cities_collection = db["cities"]
        genres_collection = db["genres"]

        if last_command == "ciudad":
            # Buscar por ciudad
            matched_city = next((c for c in cities_collection.find() if normalizar_texto(c.get("city", "")) == user_input_norm), None)
            if matched_city:
                city_id = matched_city["_id"]
                events = list(events_collection.find({"city_id": city_id}))
                for event in events:
                    if not user_message_states.get(user_id, True):
                        break

                    datos = obtener_datos_evento(event)
                    texto = formatear_evento(event, **datos)

                    # Botones de acción
                    buttons = []
                    if event.get("url_compra_entradas"):
                        buttons.append([InlineKeyboardButton("🎟️ Comprar entradas", url=event["url_compra_entradas"])])
                    
                    if event.get("latitude") and event.get("longitude"):
                        place_doc = db["places"].find_one({"_id": event.get("place_id")})
                        nombre_lugar = place_doc["name"] if place_doc and place_doc.get("name") else "Lugar"
                        maps_url = f"https://www.google.com/maps?q={event['latitude']},{event['longitude']}"
                        buttons.append([InlineKeyboardButton(f"📍 {nombre_lugar}", url=maps_url)])

                    reply_markup = InlineKeyboardMarkup(buttons) if buttons else None

                    if event.get("event_image_url"):
                        await update.message.reply_photo(photo=event["event_image_url"])
                    await update.message.reply_text(texto, reply_markup=reply_markup, parse_mode="Markdown")
                    await asyncio.sleep(0.5)
                return

        if last_command == "artista":
            # Buscar por artista
            matched_artist = next((a for a in artists_collection.find() if normalizar_texto(a.get("artist", "")) == user_input_norm), None)
            if matched_artist:
                artist_id = matched_artist["_id"]
                events = list(events_collection.find({"artist_id": artist_id}))
                for event in events:
                    datos = obtener_datos_evento(event)
                    texto = formatear_evento(event, **datos)

                    # Botones de acción
                    buttons = []
                    if event.get("url_compra_entradas"):
                        buttons.append([InlineKeyboardButton("🎟️ Comprar entradas", url=event["url_compra_entradas"])])
                    
                    if event.get("latitude") and event.get("longitude"):
                        place_doc = db["places"].find_one({"_id": event.get("place_id")})
                        nombre_lugar = place_doc["name"] if place_doc and place_doc.get("name") else "Lugar"
                        maps_url = f"https://www.google.com/maps?q={event['latitude']},{event['longitude']}"
                        buttons.append([InlineKeyboardButton(f"📍 {nombre_lugar}", url=maps_url)])

                    reply_markup = InlineKeyboardMarkup(buttons) if buttons else None

                    if event.get("event_image_url"):
                        await update.message.reply_photo(photo=event["event_image_url"])
                    await update.message.reply_text(texto, reply_markup=reply_markup, parse_mode="Markdown")
                    await asyncio.sleep(0.5)
                return
        
        if last_command == "genero":
            # Buscar por género
            genero_traducido = traducir_genero(user_input_norm)
            if genero_traducido:
                user_input_norm = genero_traducido

            matched_genre = next((g for g in genres_collection.find() if normalizar_texto(g.get("genre", "")) == user_input_norm), None)
            if matched_genre:
                genre_id = matched_genre["_id"]
                events = list(events_collection.find({"genre_id": genre_id}))
                for event in events:
                    if not user_message_states.get(user_id, True):
                        break

                    datos = obtener_datos_evento(event)
                    texto = formatear_evento(event, **datos)

                    # Botones de acción
                    buttons = []
                    if event.get("url_compra_entradas"):
                        buttons.append([InlineKeyboardButton("🎟️ Comprar entradas", url=event["url_compra_entradas"])])
                    
                    if event.get("latitude") and event.get("longitude"):
                        place_doc = db["places"].find_one({"_id": event.get("place_id")})
                        nombre_lugar = place_doc["name"] if place_doc and place_doc.get("name") else "Lugar"
                        maps_url = f"https://www.google.com/maps?q={event['latitude']},{event['longitude']}"
                        buttons.append([InlineKeyboardButton(f"📍 {nombre_lugar}", url=maps_url)])

                    reply_markup = InlineKeyboardMarkup(buttons) if buttons else None

                    if event.get("event_image_url"):
                        await update.message.reply_photo(photo=event["event_image_url"])
                    await update.message.reply_text(texto, reply_markup=reply_markup, parse_mode="Markdown")
                    await asyncio.sleep(0.5)
                return

        await update.message.reply_text("😕 Lo siento, no encontré eventos relacionados. Prueba con otro nombre de ciudad, artista o género.")
    
    except Exception as e:
        logging.exception("❌ Error inesperado en handle_message")
        await update.message.reply_text("🚨 Ha ocurrido un error inesperado. Por favor, intenta de nuevo más tarde.")

if __name__ == '__main__':
    try:
        # Obtén el bucle de eventos actual
        loop = asyncio.get_event_loop()

        # Ejecuta la función principal en el bucle de eventos existente
        loop.run_until_complete(main())
    except Exception as e:
        logging.exception("❌ Error al iniciar el bot")
        print("❌ No se pudo iniciar el bot. Revisa la configuración.")
