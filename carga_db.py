import pandas as pd
import psycopg2
import os
import logging

# 1. Configuración de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logging.info("--- INICIANDO FASE DE CARGA (LOAD) A POSTGRESQL ---")

# 2. Rutas dinámicas
directorio_actual = os.path.dirname(os.path.abspath(__file__))
ruta_master = os.path.join(directorio_actual, '1_Extract y logs', 'master_costos_divisas.csv')

try:
    # 3. Leer el Data Mart (Archivo Maestro)
    df_master = pd.read_csv(ruta_master)
    
    # Buena práctica: Reemplazar valores nulos (NaN) por None para que PostgreSQL no falle
    df_master = df_master.where(pd.notnull(df_master), None)
    logging.info(f"Archivo maestro leído. {len(df_master)} registros listos para inyección.")

    # 4. Conexión a la Base de Datos (Pon tus credenciales reales)
    conexion = psycopg2.connect(
        host="localhost",
        database="finanzas_corp", 
        user="postgres",
        password="Ash39",   
        port="5432"
    )
    cursor = conexion.cursor()

    # 5. Crear la tabla analítica si no existe (Data Definition Language)
    query_crear_tabla = """
    CREATE TABLE IF NOT EXISTS finanzas_operativas (
        id SERIAL PRIMARY KEY,
        fecha DATE,
        departamento VARCHAR(50),
        costo_usd NUMERIC(10,2),
        moneda_base VARCHAR(10),
        valor_mxn NUMERIC(10,4),
        valor_eur NUMERIC(10,4),
        costo_real_mxn NUMERIC(15,2),
        costo_real_eur NUMERIC(15,2)
    );
    """
    cursor.execute(query_crear_tabla)

    # 6. Preparar datos e insertarlos masivamente
    registros = [tuple(x) for x in df_master.to_numpy()]
    query_insertar = """
    INSERT INTO finanzas_operativas 
    (fecha, departamento, costo_usd, moneda_base, valor_mxn, valor_eur, costo_real_mxn, costo_real_eur)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    
    cursor.executemany(query_insertar, registros)
    conexion.commit() # Guardar los cambios permanentemente
    
    logging.info(f"Éxito: Se insertaron {cursor.rowcount} registros.")
    print(f"\n✅ ¡Éxito! Pipeline completado. Se inyectaron {cursor.rowcount} registros en PostgreSQL.\n")

except Exception as e:
    logging.error(f"Error crítico en la base de datos: {e}")
    print(f"\n❌ Ocurrió un error: {e}\n")

finally:
    # 7. Cierre de conexiones
    if 'conexion' in locals() and conexion:
        cursor.close()
        conexion.close()
        logging.info("Conexión a PostgreSQL cerrada exitosamente.")