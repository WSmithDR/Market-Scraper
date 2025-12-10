import pandas as pd
import schedule
import time
import logging
from datetime import datetime
from run_scraper import run_scraper


# CONFIGURACIÓN DE LOGS

logging.basicConfig(
    filename="scheduler_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
# TAREA QUE LLAMA AL SCRAPER

def ejecutar_scraping():
    logging.info("Inicio de ejecución automática del scraper")

    try:
        all_jobs = run_scraper()
        if all_jobs:
            # Si run_scraper devuelve lista de dataframes
            combined = pd.concat(all_jobs, ignore_index=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"jobs_backup_{timestamp}.csv"
            combined.to_csv(filename, index=False)
            logging.info(f"Scraping completado exitosamente — guardado en {filename}")
        else:
            logging.info("Scraping completado — pero no se encontraron trabajos")

    except Exception as e:
        logging.error(f"Error durante la ejecución del scraper: {e}")
        print("Ocurrió un error, revisar logs.")
# PROGRAMACIÓN DEL CRON INTERNO

# ejemplo: ejecutar todos los días a las 09:00
#schedule.every().day.at("09:00").do(ejecutar_scraping) # Alternativas: 
schedule.every(1).minutes.do(ejecutar_scraping)
                                                                    # schedule.every().monday.do(ejecutar_scraping)
# LOOP INFINITO

if __name__ == "__main__":
    print("Scheduler iniciado. Presiona CTRL + C para detener.")

    while True:
        schedule.run_pending()
        time.sleep(1)