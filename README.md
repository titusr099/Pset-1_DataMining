Análisis de Compras en Instacart

Descripción del Proyecto:

Este proyecto realiza un análisis detallado de los patrones de compra en Instacart utilizando Snowflake y MageAI. Se implementó un modelo estrella (Star Schema) para estructurar los datos, permitiendo insights accionables sobre el comportamiento de los clientes.

DEBER01_DATAM/

│── data/                     # Datos sin procesar y finales

│── data_pipeline/            # Pipelines de transformación de datos

│   │── custom/               # Transformación de datos y modelo estrella (GOLD Schema)

│   │── data_loaders/         # Scripts para extracción y carga de datos

│── docs/                     # Reportes y documentación

│── notebooks/                # Jupyter Notebooks con análisis exploratorio y visualizaciones

│── scripts/                  # Scripts para conexión y pruebas con Snowflake

│── README.md                 # Documentación principal del proyecto

│── requirements.txt          # Dependencias necesarias para ejecutar el proyecto



Cómo Ejecutar el Proyecto:

1. Configuración Inicial

Asegúrate de tener las siguientes variables de entorno configuradas en tu archivo .env o en tu sistema:
🔹 Configuración de Snowflake

SNOWFLAKE_ACCOUNT=<TU_CUENTA>

SNOWFLAKE_USER=<TU_USUARIO>

SNOWFLAKE_PASSWORD=<TU_CONTRASEÑA>

SNOWFLAKE_WAREHOUSE=<TU_WAREHOUSE>

SNOWFLAKE_DATABASE=<TU_DB>

SNOWFLAKE_SCHEMA=<ESQUEMA>


🔹 Configuración de MySQL

MYSQL_HOST=<TU_HOST>

MYSQL_PORT=<TU_PUERTO>

MYSQL_DATABASE=<TU_DB>

MYSQL_USER=<TU_USUARIO>

MYSQL_PASSWORD=<TU_CONTRASEÑA>




2. Instalar dependencias
Ejecuta el siguiente comando para instalar todas las dependencias necesarias:

pip install -r requirements.txt


3. Ejecución del Pipeline de Datos

Para gestionar el pipeline de datos, se utilizó Mage.AI. Puedes encontrar más detalles en su documentación oficial.
https://docs.mage.ai/introduction/overview

- Extracción de Datos desde MySQL

La extracción de datos se realiza desde una base de datos MySQL local.
El script correspondiente se encuentra en:
data_pipeline/data_loaders/extract_data.py

- Carga de Datos en Snowflake

Una vez extraídos, los datos se cargan en Snowflake utilizando el siguiente script:
data_pipeline/data_loaders/load_data.py

- Transformación y Limpieza de Datos

Los datos extraídos son transformados y normalizados antes de ser almacenados en Snowflake.
📂 data_pipeline/custom/raw_to_clean_snowflake.py

Aquí, los datos se migran del esquema RAW al CLEAN, asegurando calidad y consistencia.

🔹 Creación del Modelo Estrella

El modelo estrella se construye en el siguiente archivo:
data_pipeline/custom/start_model_dimensional.py

Esto permite estructurar los datos de forma optimizada para responder preguntas clave de negocio.

4. Análisis e Insights

Este proyecto responde preguntas clave sobre el comportamiento de compra en Instacart, incluyendo:

✔️ ¿Qué días y horas tienen más compras?

✔️ ¿Cuáles son los productos más comprados y reordenados?

✔️ ¿Cuántos productos se compran en promedio por orden?

✔️ ¿Cómo varía el comportamiento de compra según el día y la hora?


Los resultados están documentados en analysis.ipynb, con gráficos y tablas generadas.