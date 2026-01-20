import json
import os
import random
from datetime import datetime
import statistics

# Archivo donde se guardarán los datos
DATA_FILE = 'ram_data.json'

def obtener_precio_actual():
    """
    Aquí deberías conectar con una API real o hacer Web Scraping.
    Para este ejemplo, simulamos el precio de un módulo de 32GB DDR5
    siguiendo la tendencia de mercado de 2026 (aprox $180 - $220).
    """
    # SIMULACIÓN: Precio base fluctuando
    precio_base = 210.00 
    variacion = random.uniform(-5.0, 8.0) # Volatilidad diaria
    return round(precio_base + variacion, 2)

def calcular_decision(precio_actual, historico):
    if len(historico) < 5:
        return "RECOPILANDO DATOS (Faltan muestras)"
    
    precios = [d['precio'] for d in historico]
    media_movil = statistics.mean(precios[-7:]) # Media de la última semana
    precio_minimo_historico = min(precios)
    
    # Lógica de inversión
    if precio_actual < media_movil * 0.95:
        return "¡COMPRA FUERTE! (Precio 5% bajo la media)"
    elif precio_actual < media_movil:
        return "COMPRA (Precio bajo la media)"
    elif precio_actual > media_movil * 1.10:
        return "NO COMPRES (Precio disparado)"
    else:
        return "MANTENER / ESPERAR"

def actualizar_datos():
    # 1. Cargar datos anteriores
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            datos = json.load(f)
    else:
        datos = []

    # 2. Obtener nuevo dato
    precio_hoy = obtener_precio_actual()
    fecha_hoy = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 3. Calcular recomendación
    decision = calcular_decision(precio_hoy, datos)

    nuevo_registro = {
        "fecha": fecha_hoy,
        "precio": precio_hoy,
        "decision": decision
    }

    datos.append(nuevo_registro)
    
    # Mantener solo los últimos 100 registros para no saturar la gráfica
    if len(datos) > 100:
        datos = datos[-100:]

    # 4. Guardar JSON para la web
    with open(DATA_FILE, 'w') as f:
        json.dump(datos, f, indent=4)
    
    print(f"Datos actualizados: {precio_hoy}$ - {decision}")

if __name__ == "__main__":
    actualizar_datos()
