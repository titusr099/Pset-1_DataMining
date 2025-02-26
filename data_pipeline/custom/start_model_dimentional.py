if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
from mage_ai.io.snowflake import Snowflake
import os
import pandas as pd

@custom
def transform_custom(*args, **kwargs):
    """
    Crea las tablas en Snowflake en el schema GOLD si no existen, 
    transforma los datos desde CLEAN y los sube.
    """

    with Snowflake(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema="GOLD",  # subimos a gold
    ) as sf:
        
        # ---- CREACIÓN DE TABLAS EN EL SCHEMA GOLD ----
        create_table_queries = [
            """CREATE TABLE IF NOT EXISTS FactOrderProducts (
                fact_order_product_key INTEGER AUTOINCREMENT PRIMARY KEY,
                order_id INTEGER,
                order_number INTEGER,
                days_since_prior_order INTEGER,
                time_key INTEGER,
                user_key INTEGER,
                product_key INTEGER,
                add_to_cart_order INTEGER,
                reordered INTEGER
            )""",
            """CREATE TABLE IF NOT EXISTS DimTime (
                time_key INTEGER AUTOINCREMENT PRIMARY KEY,
                order_dow INTEGER,
                order_dow_name STRING,
                order_hour_of_day INTEGER
            )""",
            """CREATE TABLE IF NOT EXISTS DimUser (
                user_key INTEGER AUTOINCREMENT PRIMARY KEY,
                user_id INTEGER
            )""",
            """CREATE TABLE IF NOT EXISTS DimProduct (
                product_key INTEGER AUTOINCREMENT PRIMARY KEY,
                product_id INTEGER,
                product_name STRING,
                aisle STRING,
                department STRING
            )"""
        ]
        
        # Ejecutar la creación de tablas en GOLD
        for query in create_table_queries:
            sf.execute(query)

        print("✅ Tablas creadas/verificadas en GOLD en Snowflake")

        # ---- CARGAR LOS DATOS DESDE CLEAN ----
        df_orders = sf.load('SELECT * FROM "CLEAN"."orders"')
        df_products = sf.load('SELECT * FROM "CLEAN"."products"')
        df_order_products = sf.load('SELECT * FROM "CLEAN"."order_products"')

        # ---- CREACIÓN DE DIMENSIONES ----
        
        # DimTime
        df_dim_time = df_orders[['order_dow', 'order_hour_of_day']].drop_duplicates().reset_index(drop=True)
        df_dim_time['order_dow_name'] = df_dim_time['order_dow'].map({
            0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday',
            4: 'Thursday', 5: 'Friday', 6: 'Saturday'
        })
        df_dim_time.insert(0, 'time_key', range(1, len(df_dim_time) + 1))

        # DimUser
        df_dim_user = df_orders[['user_id']].drop_duplicates().reset_index(drop=True)
        df_dim_user.insert(0, 'user_key', range(1, len(df_dim_user) + 1))

        # DimProduct
        df_aisles = sf.load('SELECT * FROM "CLEAN"."aisles"')
        df_departments = sf.load('SELECT * FROM "CLEAN"."departments"')

        df_dim_product = df_products.merge(df_aisles, on='aisle_id', how='left')\
                                    .merge(df_departments, on='department_id', how='left')\
                                    [['product_id', 'product_name', 'aisle', 'department']]
        df_dim_product.insert(0, 'product_key', range(1, len(df_dim_product) + 1))

        # ---- CREACIÓN DE LA TABLA DE HECHOS ----
        df_fact_order_products = df_order_products.merge(df_orders, on='order_id', how='left')\
            .merge(df_dim_time, on=['order_dow', 'order_hour_of_day'], how='left')\
            .merge(df_dim_user, on=['user_id'], how='left')\
            .merge(df_dim_product, on=['product_id'], how='left')\
            [['order_id', 'order_number', 'days_since_prior_order', 'time_key', 'user_key', 'product_key', 'add_to_cart_order', 'reordered']]

        df_fact_order_products.insert(0, 'fact_order_product_key', range(1, len(df_fact_order_products) + 1))

        # ---- CARGA DE TABLAS A SNOWFLAKE (SCHEMA GOLD) ----
        sf.export(df_dim_time, "DimTime", if_exists="replace")
        sf.export(df_dim_user, "DimUser", if_exists="replace")
        sf.export(df_dim_product, "DimProduct", if_exists="replace")
        sf.export(df_fact_order_products, "FactOrderProducts", if_exists="replace")

        print("✅ Modelo estrella subido a GOLD en Snowflake")

    return {
        "df_dim_time": df_dim_time.shape,
        "df_dim_user": df_dim_user.shape,
        "df_dim_product": df_dim_product.shape,
        "df_fact_order_products": df_fact_order_products.shape
    }

@test
def test_output(output, *args) -> None:
    """
    Prueba para verificar que la transformación se ejecutó correctamente.
    """
    assert output is not None, 'El output está vacío'
    assert isinstance(output, dict), 'El output no es un diccionario'
    assert all(isinstance(value, tuple) for value in output.values()), 'Los valores de output no tienen la estructura esperada'
    print("Test superado: Datos procesados correctamente.")