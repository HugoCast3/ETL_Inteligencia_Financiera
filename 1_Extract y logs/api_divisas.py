import requests
import pandas as pd
import logging
import os
from datetime import datetime, timedelta

# ==========================================
# 1. CONFIGURACIÓN DEL SISTEMA DE MONITOREO
# ==========================================
# Aseguramos que la carpeta logs exista para evitar el FileNotFoundError
os.makedirs('../logs', exist_ok=True)

logging.basicConfig(
    filename=r'../logs/pipeline_financiero.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("--- INICIANDO EXTRACCIÓN DE DIVISAS ---")

# ==========================================
# 2. DEFINICIÓN DINÁMICA DE PARÁMETROS
# ==========================================
# Calculamos la fecha de hoy y la de hace 30 días automáticamente
fecha_fin = datetime.now().date()
fecha_inicio = fecha_fin - timedelta(days=30)

# Endpoint: Valor del Dólar (USD) frente al Peso Mexicano (MXN) y Euro (EUR)
url = f"https://api.frankfurter.app/{fecha_inicio}..{fecha_fin}?from=USD&to=MXN,EUR"

print(f"Conectando a la API del Banco Central Europeo...\nPeriodo: {fecha_inicio} al {fecha_fin}\n")

# ==========================================
# 3. EXTRACCIÓN (EXTRACT)
# ==========================================
try:
    respuesta = requests.get(url)
    
    if respuesta.status_code == 200:
        datos_json = respuesta.json()
        historico_tasas = datos_json.get('rates', {})
        
        if historico_tasas:
            lista_divisas = []
            
            # Desarmamos el JSON (que viene con fechas como llaves)
            for fecha, valores in historico_tasas.items():
                lista_divisas.append({
                    'Fecha': fecha,
                    'Moneda_Base': 'USD',
                    'Valor_MXN': valores.get('MXN'),
                    'Valor_EUR': valores.get('EUR')
                })
            
            # Convertimos a DataFrame de Pandas
            df_divisas = pd.DataFrame(lista_divisas)
            
            logging.info(f"Extracción exitosa: {len(df_divisas)} días de histórico obtenidos.")
            print("✅ ¡Datos extraídos correctamente!\n")
            print(df_divisas.tail(10).to_string(index=False)) # Mostramos los últimos 10 días
            # ==========================================
            # GUARDADO DINÁMICO (A prueba de errores)
            # ==========================================
            # 1. Detectar la carpeta exacta donde vive este script
            directorio_actual = os.path.dirname(os.path.abspath(__file__))
            
            # 2. Unir esa carpeta con el nombre de nuestro archivo
            ruta_csv = os.path.join(directorio_actual, 'tasas_crudas.csv')
            
            # 3. Guardar el DataFrame
            df_divisas.to_csv(ruta_csv, index=False)
            
            logging.info(f"Archivo guardado exitosamente en: {ruta_csv}")
            print(f"Archivo generado en: {ruta_csv}")
        else:
            logging.warning("La API respondió, pero no hay datos de tasas en ese rango de fechas.")
            print("No se encontraron datos.")
            
    else:
        logging.error(f"Error de conexión. HTTP: {respuesta.status_code}")
        print(f"Error HTTP: {respuesta.status_code}")

except Exception as e:
    logging.critical(f"Fallo catastrófico en la ejecución: {e}")
    print(f"Error en el script: {e}")

