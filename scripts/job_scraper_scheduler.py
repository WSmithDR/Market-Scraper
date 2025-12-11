import os
import schedule
import time
import logging
from datetime import datetime
import papermill as pm

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper_scheduler.log"),
        logging.StreamHandler()
    ]
)

def run_notebook(notebook_path, output_dir=None, parameters=None):
    """
    Ejecuta un notebook de Jupyter usando Papermill.
    
    Args:
        notebook_path (str): Ruta al notebook de entrada
        output_dir (str, optional): Directorio para guardar el notebook ejecutado
        parameters (dict, optional): Parámetros para inyectar al notebook
    
    Returns:
        tuple: (éxito, ruta_del_archivo_ejecutado)
    """
    try:
        # Configurar directorio de salida
        if output_dir is None:
            output_dir = os.path.join(
                os.path.dirname(notebook_path),
                "executed_notebooks"
            )
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Nombre del archivo de salida
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = os.path.join(
            output_dir,
            f"executed_{os.path.basename(notebook_path).replace('.ipynb', '')}_{timestamp}.ipynb"
        )
        
        logging.info(f"📖 Ejecutando notebook: {notebook_path}")
        logging.info(f"💾 Guardando salida en: {output_path}")
        
        # Ejecutar el notebook
        pm.execute_notebook(
            notebook_path,
            output_path,
            parameters=parameters or {},
            kernel_name='python3'
        )
        
        logging.info("✅ Notebook ejecutado exitosamente")
        return True, output_path
            
    except Exception as e:
        error_msg = f"❌ Error al ejecutar el notebook: {str(e)}"
        logging.error(error_msg)
        import traceback
        logging.error(traceback.format_exc())
        return False, None

def ejecutar_scraping():
    """Función que será ejecutada por el scheduler"""
    print("\n" + "="*50)
    start_time = datetime.now()
    logging.info(f"🕒 Iniciando ejecución programada - {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Rutas
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    notebook_path = os.path.join(base_dir, "notebooks/01. job_scrapper.ipynb")
    output_dir = os.path.join(base_dir, "executed_notebooks")
    logs_dir = os.path.join(base_dir, "execution_logs")
    
    # Crear directorios si no existen
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)
    
    # Archivo de log para esta ejecución
    log_file = os.path.join(
        logs_dir,
        f"scraper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )
    
    # Configurar file handler adicional
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(file_handler)
    
    try:
        # Ejecutar el notebook
        success, output_path = run_notebook(
            notebook_path=notebook_path,
            output_dir=output_dir,
            parameters={
                'execution_time': start_time.isoformat(),
                'output_dir': output_dir
            }
        )
        
        if success:
            logging.info(f"📊 Resultados guardados en: {output_path}")
        else:
            logging.error("❌ Falló la ejecución del notebook")
            
    except Exception as e:
        logging.error(f"❌ Error inesperado: {str(e)}")
        import traceback
        logging.error(traceback.format_exc())
    
    finally:
        # Cerrar y remover el file handler
        file_handler.close()
        logging.getLogger().removeHandler(file_handler)
        
        execution_time = (datetime.now() - start_time).total_seconds()
        logging.info(f"🏁 Finalizado en {execution_time:.2f} segundos")
        print("="*50 + "\n")

def get_valid_time():
    """Solicita una hora válida al usuario"""
    from datetime import datetime, time as dt_time, timedelta
    
    while True:
        try:
            time_str = input("\nIngrese la hora en formato 24h (HH:MM): ")
            hour, minute = map(int, time_str.split(':'))
            
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                print("Error: Hora inválida. Use formato 24h (00:00 - 23:59)")
                continue
                
            now = datetime.now()
            scheduled_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            if scheduled_time < now:
                print(f"\n¡Atención! La hora ingresada ({time_str}) ya ha pasado hoy.")
                print(f"El scraping se programará para mañana a las {time_str}.")
                scheduled_time += timedelta(days=1)
            
            confirm = input(f"\n¿Desea programar el scraping para {scheduled_time.strftime('%Y-%m-%d %H:%M')}? (s/n): ").lower()
            if confirm == 's':
                return time_str
                
        except ValueError:
            print("Formato inválido. Por favor use HH:MM (ej: 09:30 o 14:15)")

def setup_scheduler():
    """Configura el programador de tareas"""
    print("\n=== Configuración del Programador de Scraping ===")
    print("Ingrese la hora en que desea que se ejecute el scraping diariamente.")
    
    time_str = get_valid_time()
    schedule.every().day.at(time_str).do(ejecutar_scraping).tag('daily_scraping')
    print(f"\n✓ Scraping programado para ejecutarse diariamente a las {time_str}")
    
    # Para pruebas: ejecutar cada 1 minuto
    # schedule.every(1).minutes.do(ejecutar_scraping).tag('test_run')

if __name__ == "__main__":
    print("="*50)
    print("🚀 Iniciando Scheduler de Scraping")
    print(f"🕒 Hora actual: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Presiona Ctrl+C para detener")
    print("="*50)
    
    setup_scheduler()
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDeteniendo el scheduler...")
        schedule.clear()
        print("Scheduler detenido correctamente")
    except Exception as e:
        logging.error(f"Error en el scheduler: {str(e)}")
        raise