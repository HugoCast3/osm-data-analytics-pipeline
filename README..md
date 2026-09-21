#  End-to-End Data Engineering & Analytics Pipeline: Sports Analytics

##  Resumen del Proyecto
Este proyecto simula un entorno corporativo de **Business Intelligence y Data Engineering** aplicado a estadísticas deportivas (OSM Analytics). El objetivo fue diseñar una arquitectura de datos relacional robusta, automatizar la ingesta y limpieza de datos, y desplegar un dashboard interactivo, eliminando procesos manuales y reduciendo el margen de error.

## Stack Tecnológico
* **Base de Datos:** PostgreSQL (Modelo Estrella, Multi-JOINs, CTEs, Window Functions, Triggers, Stored Procedures).
* **ETL Pipeline:** Python (Pandas para limpieza y manejo de nulos, `psycopg2` para inyección masiva).
* **Visualización:** Power BI (Conexión DirectQuery/Import a servidor local, modelado y KPIs interactivos).

##  Arquitectura del Flujo de Datos (Data Flow)
1. **Extracción y Transformación (Python/Pandas):** 
   Se procesan datos crudos simulando extracciones de sistemas fuente. Se aplica limpieza de cadenas de texto (`.strip().title()`), manejo de valores nulos (Data Imputation) y casteos de tipos de datos.
2. **Carga (PostgreSQL):** 
   Inyección masiva y segura mediante `executemany` evitando inyecciones SQL.
3. **Modelado y Reglas de Negocio (SQL):**
   * Creación de una Tabla de Hechos (`Partidos`) con doble llave foránea (Self-Referencing) hacia la dimensión de `Equipos`.
   * Vistas materializadas que aplican lógica condicional (`CASE WHEN`) para asignar puntajes.
   * Uso de Funciones de Ventana (`RANK()`) y `UNION ALL` para calcular la tabla general de clasificación dinámicamente.
4. **Visualización (Power BI):** 
   Consumo directo de las vistas de PostgreSQL para mostrar el ranking de jugadores y el desempeño histórico de la liga en tiempo real.

##  Vista Previa del Dashboard
*(Sube aquí la captura de pantalla de tu dashboard: `![Dashboard](3_Business_Intelligence/dashboard_1.png)`)*