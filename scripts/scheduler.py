import schedule
import time
import subprocess

def run_main():
    print("🚀 Ejecutando la actualización de eventos...")
    subprocess.run(["python", "main.py"])

# Programar ejecución diaria
schedule.every().day.at("06:00").do(run_main)

print("🕕 Scheduler activado: La actualización diaria se ejcutará a las 6 AM.")

while True:
    schedule.run_pending()
    time.sleep(60)  # Revisar cada minuto si hay tareas pendientes