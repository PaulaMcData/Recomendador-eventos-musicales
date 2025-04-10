<p align="center">
  <img src="https://raw.githubusercontent.com/PaulaMcData/Recomendador-eventos-musicales/main/assets/banner_evento_music_es.png" alt="Evento Music ES Banner" style="max-width: 60%; height: auto; object-fit: cover; object-position: center;"/>
</p>

<h1 align="center">🎶 Recomendador de Eventos Musicales</h1>

<p align="center">Proyecto del Máster en Data Science - IEBS</p>

Este proyecto es parte del Global Project del Máster en Data Science de IEBS, y tiene como objetivo desarrollar una arquitectura modular en Python capaz de recopilar, transformar, almacenar y analizar eventos musicales utilizando datos de la API de Ticketmaster, Last.fm y una base de datos MongoDB.

## 📚 Contenidos

- [Ramas](#-estructura-de-ramas-en-el-repositorio)
- [Fases proyecto](#-fases-modulares-del-proyecto-etl-mongodb-sentiment-analysis-nlp---textblob)
- [Estructura carpetas](#-estructura-de-carpetas)
- [Próximos pasos](#próximos-pasos)
- [Instalación](#-cómo-instalar-y-ejecutar-el-proyecto)
- [Bot Telegram](#-bot-de-telegram-conectado-al-sistema-render)


## 🌿 Estructura de ramas en el repositorio

Este repositorio usa tres ramas:

- `main`: congelada tras la entrega.
- `Global-Project`: copia oficial del proyecto entregado.
- `Post-Global-Project`: rama en desarrollo y mejoras.

Puedes cambiar de rama en GitHub según lo que necesites consultar.

## ✅ Fases modulares del proyecto (ETL, MongoDB, Sentiment Analysis NLP - textBlob)

El proyecto ejecuta de forma secuencial y modular los siguientes pasos:

1. 📥 **Ingesta de datos**  
   Se conecta a la API de Ticketmaster para descargar eventos musicales en ciudades de España.  
   Script: `fetch_ticketmaster_data` en `data_ingestion_020`.

2. 🔄 **Transformación de eventos**  
   Cada evento se limpia y transforma para conservar solo los campos relevantes.  
   Script: `transform_event_data` en `data_processing_021`.

3. 💾 **Almacenamiento en MongoDB**  
   Los eventos se almacenan o actualizan en la colección `events` de MongoDB Atlas.  
   Script: `save_or_update_event` + conexión con `connect_to_mongodb` en `database_022`.

4. 🧱 **Actualización de colecciones derivadas**  
   Se generan colecciones auxiliares como `artists`, `genres`, `cities`, `organizers` y `status`, extrayendo valores únicos (ids_) desde los eventos.  
   Script: `update_all_collections` en `database_022`.

5. 🧠 **Análisis de sentimiento**  
   Se conecta con la API pública de Last.fm y aplica un análisis de sentimiento a cada artista usando NLP (TextBlob).  
   Se añaden dos nuevas etiquetas: `sentiment` (positivo, neutro, negativo) y `polarity` (valor numérico).  
   Script: `sentiment_analysis` en `analysis_023`.

6. 📊 **Creación del dataset final `fact_events`**  
   Se construye una tabla de hechos `fact_events` normalizada con referencias a todas las colecciones anteriores, lista para análisis o visualización.  
   Script: `generate_fact_events` en `database_022`.

Todo el flujo anterior se ejecuta automáticamente al lanzar:

```terminal
python3 main.py
```

Desde la raíz del proyecto.

## 📁 Estructura de carpetas

```
Recomendador-eventos-musicales/
├── config_01/               # Configuración general del proyecto (API keys, constantes)
├── src_02/                  # Módulos funcionales del pipeline
│   ├── data_ingestion_020/
│   ├── data_processing_021/
│   ├── database_022/
│   ├── analysis_023/
│   ├── bot_024/
├── docGP_03/                # Documentación Word y presentación de Global Project
├── main.py                  # Script principal de ejecución del flujo
├── README.md                # Documentación del proyecto
├── .venv/                   # Entorno virtual local (excluido del control de versiones)
├── .vscode/                 # launch.json para ejecutar debugger (excluido del control de versiones)
├── .env                     # Credenciales de acceso a APIS (excluido del control de versiones)
├── .env.example             # Plantilla para rellenar credenciales de acceso a APIS de otro usuario
├── .gitignore               # Todo aquello que se excluye del control de versiones
└── requirements.txt         # Bibliotecas necesarias para ejecutar los scripts
```

## Próximos pasos

- 📊 Visualización interactiva en mapa con Folium.
- 🤖 Enriquecer la base de datos con análisis de sentimiento desde redes sociales.

## 🚀 Cómo instalar y ejecutar el proyecto

### 1. Clonar el repositorio

```terminal
git clone https://github.com/PaulaMcData/Recomendador-eventos-musicales.git
cd Recomendador-eventos-musicales
```

### 2. Crear y activar el entorno virtual

```terminal
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar credenciales

Este proyecto utiliza un archivo `.env` para cargar de forma segura las credenciales necesarias (API de Ticketmaster, MongoDB Atlas, Last.fm, etc.).

No se comparten datos sensibles en el repositorio.  
El archivo `config.py` de la carpeta `config_01/` se encarga automáticamente de leer estas variables usando `python-dotenv`.

⚠️ Para facilitar la configuración por parte de cualquier usuario, se incluye en el repositorio una plantilla llamada `.env.example`.  
Cada persona debe **duplicar ese archivo, renombrarlo como `.env`** y rellenarlo con sus propias claves.

Ejemplo:

```bash
cp .env.example .env
# Editar .env y rellenar cada clave con tus credenciales reales
```

Una vez hecho esto, puedes ejecutar el proyecto con normalidad desde `main.py`.

### 5. Ejecutar el proyecto

```terminal
python3 main.py
```
Una vez ejecutado `main.py`, la base de datos MongoDB queda actualizada con toda la información enriquecida.


## 🤖 Bot de Telegram conectado al sistema Render

Este proyecto incluye un bot de Telegram que consulta la base de datos MongoDB para recomendar eventos musicales al usuario en función de sus preferencias.

- 🔄 El bot funciona de forma **asíncrona y continua**, desplegado en la plataforma [Render](https://render.com).
- 🔗 Render está configurado para desplegar automáticamente el bot y conectarse a:
  - Este repositorio de GitHub (para desplegar los scripts).
  - La base de datos MongoDB Atlas (donde consulta la información).
- 📁 El bot está compuesto por:
  - Script principal: `src_02/bot_024/telegram_bot.py`
  - Funciones auxiliares de formato y visualización: `src_02/bot_024/formatter_bot.py`
- 🗣️ El bot responde automáticamente a comandos del usuario y muestra resultados personalizados.

#### 🔗 Acceso al bot en Telegram

<p align="center">
  <img src="https://raw.githubusercontent.com/PaulaMcData/Recomendador-eventos-musicales/main/assets/logo_telegram_bot.png" alt="Bot Telegram EventoMusicES" width="120"/>
</p>

Puedes encontrarlo en Telegram como:

`@eventomusices_bot`

No necesitas ejecutarlo manualmente. Está **activo 24/7** gracias a su despliegue en Render, y está listo para responder a cualquier usuario en tiempo real 🎧