import pandas as pd
import os
import logging

# 1. Configuración básica de log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logging.info("--- INICIANDO TRANSFORMACIÓN DE DATOS ---")

# 2. Rutas dinámicas (en la misma carpeta)
directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_costos = os.path.join(directorio_actual, 'costos_operativos.csv')
ruta_tasas = os.path.join(directorio_actual, 'tasas_crudas.csv')

try:
    # 3. LECTURA: Convertir los CSV a DataFrames
    df_costos = pd.read_csv(ruta_costos)
    df_tasas = pd.read_csv(ruta_tasas)

    logging.info("Archivos leídos correctamente. Iniciando cruce...")

    # 4. TRANSFORMACIÓN: Left Join usando la columna 'Fecha'
    # Esto unirá la tasa de cambio correspondiente al día exacto del costo
    df_master = pd.merge(df_costos, df_tasas, on='Fecha', how='left')

    # 5. ENRIQUECIMIENTO: Calcular los costos reales
    df_master['Costo_Real_MXN'] = df_master['Costo_USD'] * df_master['Valor_MXN']
    df_master['Costo_Real_EUR'] = df_master['Costo_USD'] * df_master['Valor_EUR']

    # Redondeamos a 2 decimales para formato de moneda
    df_master['Costo_Real_MXN'] = df_master['Costo_Real_MXN'].round(2)
    df_master['Costo_Real_EUR'] = df_master['Costo_Real_EUR'].round(2)

    print("\n✅ ¡Transformación y Cruce Exitoso!\n")
    print(df_master.to_string(index=False))

    # 6. GUARDAR RESULTADO (Data Mart temporal)
    ruta_salida = os.path.join(directorio_actual, 'master_costos_divisas.csv')
    df_master.to_csv(ruta_salida, index=False)
    logging.info(f"Archivo maestro generado: {ruta_salida}")

except Exception as e:
    logging.error(f"Ocurrió un error en la transformación: {e}")
    print(f"Error: {e}")