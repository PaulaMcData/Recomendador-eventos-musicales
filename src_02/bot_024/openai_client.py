# src_02/utils/openai_client.py
import openai
import os

# Carga tu API Key desde variable de entorno o un .env
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(user_input: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # optimiza para tu presupuesto
            messages=[
                {"role": "system", "content": "Eres un asistente musical amable y experto en recomendar eventos musicales."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error al generar respuesta: {e}"