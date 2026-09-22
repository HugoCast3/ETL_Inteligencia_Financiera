import subprocess
import os
import logging
import sys

# 1. Configuración del log maestro
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ejecutar_script(ruta_script, nombre_fase):
    """Función que ejecuta un script externo de Python y captura sus errores."""
    logging.info(f"--- INICIANDO FASE: {nombre_fase} ---")
    try:
        # Ejecutamos el script. check=True hace que arroje error si el script falla.
        subprocess.run([sys.executable, ruta_script], check=True, capture_output=True, text=True)
        logging.info(f"✅ FASE {nombre_fase} COMPLETADA CON ÉXITO.")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ ERROR FATAL EN FASE {nombre_fase}.")
        logging.error(f"Detalle del error del script:\n{e.stderr}")
        return False

def main():
    print("🚀 Iniciando Orquestador del Pipeline Financiero...\n")
    
    # 2. Rutas dinámicas de los scripts
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    
    script_extract = os.path.join(directorio_actual, '1_Extract y logs', 'api_divisas.py')
    script_transform = os.path.join(directorio_actual, 'transformacion.py')
    script_load = os.path.join(directorio_actual, 'carga_db.py')
    
    # 3. Flujo de ejecución condicional (Dependencias)
    if ejecutar_script(script_extract, "1. EXTRACT (Frankfurter API)"):
        
        if ejecutar_script(script_transform, "2. TRANSFORM (Pandas Merge)"):
            
            if ejecutar_script(script_load, "3. LOAD (PostgreSQL)"):
                print("\n🎉 ¡PIPELINE END-TO-END EJECUTADO EXITOSAMENTE!")
                logging.info("Ejecución total finalizada correctamente.")
            else:
                print("\n⚠️ El pipeline se abortó en la fase de CARGA.")
        else:
            print("\n⚠️ El pipeline se abortó en la fase de TRANSFORMACIÓN.")
    else:
        print("\n⚠️ El pipeline se abortó en la fase de EXTRACCIÓN.")

if __name__ == "__main__":
    main()