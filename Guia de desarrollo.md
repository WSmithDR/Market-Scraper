## 🧭 Guía de Desarrollo del Proyecto "Market Scraper"

Este proyecto se puede dividir en 5 fases principales, siguiendo una metodología ágil/iterativa, lo que permite la entrega continua de valor. 
---

### 1. ⚙️ Fase de Configuración y Planificación (Sprints 1-2)

#### 1.1. Gestión del Proyecto y Colaboración
* **Metodología:** **Scrum** o **Kanban** simple.
* **Herramientas:** **Trello** o **Jira** (para tareas y *backlog*), **Git/GitHub/GitLab** (para control de versiones).
* **Entregable Clave:** Repositorio inicial con estructura de proyecto (carpetas `src/`, `data/`, `notebooks/`, `docs/`).

#### 1.2. Pila Tecnológica Central
| Componente | Tecnología Sugerida | Razón |
| :--- | :--- | :--- |
| **Lenguaje** | **Python** | Ideal para Data Science, *Scraping* (Scrapy), y *Machine Learning*. |
| **Scraping** | **Scrapy** y/o **Selenium** | Scrapy para sitios estáticos/API. Selenium para sitios dinámicos (e.g., LinkedIn). |
| **Bases de Datos** | **MongoDB** (Principal) y **Supabase** (Reporte/API) | MongoDB es flexible para datos semi-estructurados de *scraping*. Supabase (PostgreSQL) es ideal para el almacenamiento estructurado final y la API. |
| **Orquestación** | **Docker** y **Docker Compose** | Empaquetar el *scraper* y la base de datos para garantizar la portabilidad y la fácil programación. |

---

### 2. 🎣 Fase de Extracción de Datos (*Scraping*) (Sprints 2-3)

Esta fase es el núcleo del **Market Scraper**.

#### 2.1. Desarrollo del Scraper
* **Manejo de Sitios:**
    * **Sitios Estáticos (Bolsas de Empleo):** Utilizar **Scrapy** o **BeautifulSoup** con el módulo `requests`.
    * **Sitios Dinámicos (LinkedIn, Sitios de Empresas):** Utilizar **Selenium** o **Playwright** para interactuar con JavaScript y simular la navegación del usuario.
* **Mecanismos de Control (Anti-Bloqueo):**
    * Implementar *Proxies Rotativos* o usar servicios *Scraping as a Service* (e.g., ScraperAPI) si los bloqueos son frecuentes.
    * Configurar *delays* (**Scrapy AUTOTHROTTLE**) para simular un comportamiento humano y cumplir con la política de uso del sitio.
    * Implementar gestión de *cookies* y *headers* de sesión.
* **Extracción de Información de la Empresa (Enriquecimiento):**
    * Después de obtener el nombre de la empresa de una vacante, el *scraper* debe hacer una consulta secundaria (ej. una API como Clearbit o simplemente Google/LinkedIn) para obtener el **tamaño, la industria, y el contacto general**.

#### 2.2. Programación y Orquestación
* El Full Stack Developer debería usar **Docker** para crear una imagen del *scraper* con todas las dependencias.
* **Programación (Scheduling):** Usar **Docker Compose** o una herramienta de orquestación (como **Apache Airflow** o un simple **Cron Job** dentro de un contenedor) para ejecutar el *scraper* a intervalos definidos.

---

### 3. ✨ Fase ETL (*Extraction, Transformation, Loading*) (Sprints 3-4)

Los Científicos de Datos liderarán esta fase, esencial para la calidad del análisis.

#### 3.1. Pipeline de Limpieza (T de Transformación)
* **Normalización de Texto:**
    * **Roles:** Normalizar nombres de roles (ej. "Data Sci", "Data Scientist", "Científico de Datos" $\rightarrow$ **Científico de Datos**).
    * **Tecnologías:** Extracción y normalización de *skills* (ej. "Pyth", "Pithon" $\rightarrow$ **Python**). Usar **expresiones regulares (regex)** y **NLP básico**.
* **Limpieza de Datos:** Eliminar duplicados basándose en una combinación de título, empresa y ubicación.
* **Estandarización:** Convertir los niveles de *seniority* (Junior, Mid, Senior) a un formato consistente.
* **Filtrado:** Aplicar los filtros requeridos (país, industria, etc.) en esta etapa.

#### 3.2. Almacenamiento Estructurado (L de Loading)
* Los datos limpios deben migrarse de la base de datos inicial (MongoDB) a la base de datos final **Supabase (PostgreSQL)** en un esquema tabular bien definido.
* **Esquema de Tabla Sugerido:**

| Campo | Tipo de Dato | Propósito |
| :--- | :--- | :--- |
| `id_vacante` | UUID | Identificador Único |
| `titulo_normalizado` | String | Título del rol estandarizado |
| `empresa_nombre` | String | Nombre de la empresa |
| `empresa_tamano` | String | (Pequeña, Mediana, Grande) |
| `pais` | String | Ubicación (normalizado) |
| `seniority` | String | Nivel de experiencia (J, M, S) |
| `fecha_extraccion` | Timestamp | Cuándo se extrajo el dato |
| `skills_list` | Array de Strings | Lista de tecnologías clave extraídas |

---

### 4. 📊 Fase de Análisis y Reporte (Sprints 4-5)

Esta fase es totalmente de dominio de los Científicos de Datos.

#### 4.1. Análisis de Tendencias
* **Herramientas:** **Jupyter Notebooks** (con `pandas`, `numpy`), y **Plotly** o **Matplotlib** para visualización.
* **Métricas Clave:**
    * **Crecimiento de Demanda:** Calcular la variación porcentual de vacantes por rol/skill en el tiempo.
    * ***Skills* Emergentes:** Identificar las *skills* con el mayor aumento de menciones en el último periodo.
    * **Distribución Geográfica/Sectorial:** Mapa de calor de la demanda de roles específicos.
* **Integración:** Usar la API de Supabase para consultar directamente los datos limpios.

#### 4.2. Entregable de Reporte
* **Opciones de Dashboard/Notebook:**
    * **Jupyter Notebook:** Para un reporte técnico.
    * **Streamlit/Dash:** El Full Stack Developer puede construir un *dashboard* simple y rápido con estas herramientas, consumiendo la **API de Supabase**. Esto permite un reporte automático y dinámico.

---

### 5. 📚 Fase de Documentación y Entrega (Sprint 5)

* **Documentación del Código:**
    * Documentar el *scraper* (`README.md`) con instrucciones claras sobre cómo instalar, configurar variables de entorno y ejecutarlo con Docker.
    * Utilizar *docstrings* en el código Python.
* **Documentación del Análisis:** Asegurar que el *notebook* de *insights* contenga las conclusiones y la interpretación de las tendencias.
* **Entrega Final:** Los entregables solicitados son:
    * **Dataset de 500+ registros procesados:** Entregado en la base de datos Supabase y exportable (CSV/JSON).
    * **Script documentado y automatizable:** Repositorio en GitHub con el código Python y el `Dockerfile`.
    * **Reporte de insights:** Notebook o dashboard en Streamlit/Dash.

---

## 🛠️ Conclusión de la Pila Tecnológica

| Rol | Foco Principal | Tecnologías Clave |
| :--- | :--- | :--- |
| **Científicos de Datos** | Desarrollo del Scraper, ETL, Análisis de Tendencias | **Python**, **Scrapy**, **Pandas**, **Regex**, **MongoDB** (Input), **Supabase** (Output) |
| **Full Stack Developer** | Infraestructura, Orquestación, Dashboard de Reporte | **Docker**, **Airflow/Cron**, **Supabase API**, **Streamlit/Dash** |

La combinación de **Python/Scrapy** para la recolección, **MongoDB** para la ingesta flexible, **Supabase/PostgreSQL** para el almacenamiento estructurado final, y **Docker** para la automatización, proporciona una solución robusta y escalable que se alinea perfectamente con las habilidades de su equipo.