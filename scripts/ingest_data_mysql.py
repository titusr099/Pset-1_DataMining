import pymysql
import pandas as pd
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración de conexión a MySQL usando variables de entorno
db_config = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE")
}

# Conectar a MySQL
connection = pymysql.connect(
    host=db_config["host"], 
    user=db_config["user"], 
    password=db_config["password"]
)
cursor = connection.cursor()

# Eliminar la base de datos si ya existe y crearla de nuevo
cursor.execute(f"DROP DATABASE IF EXISTS {db_config['database']};")
cursor.execute(f"CREATE DATABASE {db_config['database']};")
cursor.execute(f"USE {db_config['database']};")

# Definir tablas con la actualización en `orders`
table_definitions = {
    "aisles": """
        CREATE TABLE IF NOT EXISTS aisles (
            aisle_id INT PRIMARY KEY,
            aisle VARCHAR(255)
        );
    """,
    "departments": """
        CREATE TABLE IF NOT EXISTS departments (
            department_id INT PRIMARY KEY,
            department VARCHAR(255)
        );
    """,
    "orders": """
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT,
            user_id INT,
            order_number INT,
            order_dow INT,
            order_hour_of_day INT,
            days_since_prior_order FLOAT
        );
    """,
    "products": """
        CREATE TABLE IF NOT EXISTS products (
            product_id INT PRIMARY KEY,
            product_name VARCHAR(255),
            aisle_id INT,
            department_id INT
        );
    """,
    "order_products": """
        CREATE TABLE IF NOT EXISTS order_products (
            order_id INT,
            product_id INT,
            add_to_cart_order INT,
            reordered INT,
            PRIMARY KEY (order_id, product_id)
        );
    """
}

# Crear tablas en MySQL
for table, query in table_definitions.items():
    cursor.execute(query)
    print(f"Tabla {table} creada")

# Cargar archivos CSV
data_folder = os.path.abspath("data")  # Obtiene la ruta absoluta correcta
csv_files = {
    "aisles": "aisles.csv",
    "departments": "departments.csv",
    "orders": "instacart_orders.csv",
    "products": "products.csv",
    "order_products": "order_products.csv"
}

# Función para cargar CSV en MySQL
def load_csv_to_mysql(file_name, table_name):
    file_path = os.path.abspath(os.path.join(data_folder, file_name))
    print(f"PATH_FILE: {file_path}")
    df = pd.read_csv(file_path, sep=";")

    # Convertir NaN en None para evitar errores en MySQL
    df = df.astype(object).where(pd.notna(df), None)

    # Generar consulta SQL dinámica
    cols = ",".join(df.columns)
    placeholders = ",".join(["%s"] * len(df.columns))
    query = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"

    # Insertar datos fila por fila
    cursor.executemany(query, df.values.tolist())

    connection.commit()
    print(f"Datos insertados en {table_name} ({len(df)} filas).")

# Cargar los datos en las tablas
for table, file in csv_files.items():
    load_csv_to_mysql(file, table)

# Cerrar conexión
cursor.close()
connection.close()
print("Carga de datos completada.")
