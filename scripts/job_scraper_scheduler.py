import os
import time
import logging
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import schedule
from datetime import datetime

# CONFIGURACIÓN DE LOGS
logging.basicConfig(
    filename="scheduler_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def execute_notebook(notebook_path):
    """Ejecuta un notebook de Jupyter programáticamente usando nbconvert"""
    try:
        print(f"📖 Cargando notebook desde: {notebook_path}")
        
        # Configuración del ejecutor
        ep = ExecutePreprocessor(
            timeout=600,  # 10 minutos de timeout
            kernel_name='market_scrapper_kernel',
            allow_errors=True,
            interrupt_on_timeout=True
        )
        
        # Ruta de salida para el notebook ejecutado
        notebook_dir = os.path.dirname(notebook_path)
        notebook_name = os.path.basename(notebook_path)
        output_path = os.path.join(notebook_dir, f"executed_{notebook_name}")
        
        print("⚙️  Configurando el entorno de ejecución...")
        print(f"   - Directorio de trabajo: {notebook_dir}")
        print(f"   - Kernel: python3")
        
        # Leer el notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        
        print("▶️  Iniciando ejecución del notebook...")
        start_time = time.time()
        
        try:
            # Ejecutar el notebook completo
            ep.preprocess(nb, {'metadata': {'path': notebook_dir}})
            
            # Guardar el notebook ejecutado
            with open(output_path, 'w', encoding='utf-8') as f:
                nbformat.write(nb, f)
            
            print(f"✅ Notebook ejecutado y guardado en: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error durante la ejecución: {str(e)}")
            return False
            
    except Exception as e:
        error_msg = f"❌ Error crítico: {str(e)}"
        print(error_msg)
        logging.error(error_msg)
        import traceback
        traceback.print_exc()
        return False
    finally:
        execution_time = time.time() - start_time
        print(f"⏱️  Tiempo de ejecución: {execution_time:.2f} segundos")


def ejecutar_scraping():
    print("\n" + "="*50)
    print(f"🕒 Iniciando ejecución programada - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info("Inicio de ejecución automática del notebook de scraping")
    
    # Ruta al notebook
    notebook_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),  # Go up one level from scripts/
        "notebooks/01. job_scrapper.ipynb"
    )
    
    print(f"🔍 Buscando notebook en: {notebook_path}")
    
    if not os.path.exists(notebook_path):
        error_msg = f"❌ No se encontró el notebook en: {notebook_path}"
        logging.error(error_msg)
        print(error_msg)
        return

    try:
        print("🚀 Iniciando ejecución del notebook...")
        success = execute_notebook(notebook_path)
        if success:
            msg = "✨ Ejecución del notebook completada exitosamente"
            logging.info(msg)
            print(msg)
        else:
            error_msg = "❌ Error al ejecutar el notebook, revisa los logs"
            logging.error(error_msg)
            print(error_msg)
            
    except Exception as e:
        error_msg = f"❌ Error inesperado: {str(e)}"
        logging.error(error_msg)
        print(error_msg)
    finally:
        print(f"🏁 Finalizado - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*50 + "\n")



# Programar la ejecución diaria a las 9:00 AM
schedule.every().day.at("09:55").do(ejecutar_scraping)

# Para pruebas, puedes descomentar esta línea para ejecutar cada minuto
# schedule.every(1).minutes.do(ejecutar_scraping)

if __name__ == "__main__":
    print("Scheduler iniciado. Presiona CTRL + C para detener.")
    print(f"Se ejecutará el notebook: notebooks/01. job_scrapper.ipynb")
    
    # Ejecutar inmediatamente al inicio (opcional)
    # ejecutar_scraping()
    
    while True:
        schedule.run_pending()
        time.sleep(1)