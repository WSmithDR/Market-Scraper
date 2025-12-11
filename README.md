# Job Market Scraper

##  Descripción

Market Scraper es una herramienta de análisis de mercado diseñada para **automáticamente recolectar, procesar y estructurar información de vacantes, empresas y tendencias relevantes** desde múltiples fuentes públicas.  
El proyecto busca **centralizar datos dispersos**, enriquecerlos y permitir su análisis para detectar oportunidades, patrones de demanda y cambios en el mercado laboral y sectorial. 

---

##  Objetivos del Proyecto

- 📥 **Recolectar datos de múltiples fuentes**, incluyendo sitios de empleo y plataformas profesionales.  
- 🧠 **Filtrar y clasificar** la información por industria, país, tipo de rol y nivel de seniority.   
- 📊 **Estructurar y enriquecer los datasets** con atributos clave (e.g., tamaño de empresa, industria principal).  
- 📈 **Generar insights accionables** para análisis, visualizaciones o integración con dashboards. 

---

##  Requerimientos Técnicos

El proyecto está diseñado para usar tecnologías modernas de scraping, procesamiento y análisis:

- 🔹 **Lenguaje principal:** Python   
- 🔹 **Scraping programado** con control de frecuencia y manejo de dinámicas web  
- 🔹 **Pipeline ETL** para limpieza, normalización y enriquecimiento de datos 
- 🔹 **Base de datos:**  MongoDB para almacenamiento estructurado
- 🔹 **Visualización de datos :** Power BI

---

## 📁 Estructura del Repositorio

/Market-Scraper
│── /data # Datasets crudos y procesados
│── /docs # Documentación y guías
│── /notebooks # Notebooks de análisis y demo
│── /operations # Pipelines y scripts automatizados
│── /src # Código principal
│── /test # Tests y validaciones
│── /utils # Utilidades de apoyo
├── Guia de desarrollo.md # Guía de trabajo y estilo
├── requirements.txt # Dependencias del proyecto
├── run_scraper.py # Script principal para ejecutar scrapers
├── Scheduler.py # Lógica de scheduling / automatización


👥 Equipo & Créditos
Scraping de distintas plataformas → Wagner Dueñas
Limpieza y transformación (ETL) → Gianluca Lambruschini
Automatización → Marlene Maraz
Visualización y análisis → Julia Panei


🔗 Enlaces útiles
Repositorio GitHub: https://github.com/WSmithDR/Market-Scraper
Trello del equipo: https://trello.com/invite/b/68de93cabfbfdcc957c1f8a5/ATTI9c011b9f0e701d419ced427f42977b89945854A3/market-scrapper 
Dashboards (Power BI): https://drive.google.com/file/d/1ymU9HVExUs0Q57AZyxZvtUWM1rfV1dKo/view?usp=sharing

📑 Guía de desarrollo: docs/Guia de desarrollo.md

📊 Notebooks de análisis: notebooks/
