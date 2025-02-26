if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
from mage_ai.io.snowflake import Snowflake
import os

@custom
def transform_custom(*args, **kwargs):
    """
    Extrae los datos del esquema RAW en Snowflake, los limpia y los guarda en el esquema CLEAN.
    """
    # Conectar a Snowflake usando variables de entorno 
    with Snowflake(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema="RAW",  # Leer desde el esquema RAW
    ) as sf:

        # Extraer datos del esquema RAW
        queries = {
            "orders": 'SELECT * FROM "orders"',
            "products": 'SELECT * FROM "products"',
            "order_products": 'SELECT * FROM "order_products"',
            "aisles": 'SELECT * FROM "aisles"',
            "departments": 'SELECT * FROM "departments"'
        }

        df_orders = sf.load(queries["orders"])
        df_products = sf.load(queries["products"])
        df_order_products = sf.load(queries["order_products"])
        df_aisles = sf.load(queries["aisles"])
        df_departments = sf.load(queries["departments"])

    # --- LIMPIEZA DE DATOS ---
    if not df_order_products.empty:
        df_order_products['add_to_cart_order'] = df_order_products['add_to_cart_order'].fillna(-1)

    if not df_orders.empty:
        df_orders['days_since_prior_order'] = df_orders['days_since_prior_order'].fillna(0)

    if not df_products.empty:
        df_products['product_name'] = df_products['product_name'].fillna("Producto desconocido")

    # --- CARGA DE DATOS EN EL ESQUEMA CLEAN ---
    with Snowflake(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema="CLEAN",  # Guardar en el esquema CLEAN
    ) as sf:

        for table_name, df in {
            "orders": df_orders,
            "products": df_products,
            "order_products": df_order_products,
            "aisles": df_aisles,
            "departments": df_departments
        }.items():
            if not df.empty:  # Evita exportar tablas vacías
                sf.export(df, table_name, if_exists="replace")
                print(f"✅ Tabla {table_name} cargada exitosamente en CLEAN.")

    print("Proceso completado: Datos limpios y cargados en CLEAN.")

    return {
        "df_orders": df_orders.shape,
        "df_products": df_products.shape,
        "df_order_products": df_order_products.shape,
        "df_aisles": df_aisles.shape,
        "df_departments": df_departments.shape
    }

@test
def test_output(output, *args) -> None:
    """
    Prueba para verificar que la transformación y carga de datos se ejecutó correctamente.
    """
    assert output is not None, 'El output está vacío'
    assert isinstance(output, dict), 'El output no es un diccionario'
    assert all(isinstance(value, tuple) for value in output.values()), '❌ Los valores de output no tienen la estructura esperada'
    
    print("✅ Test superado: Datos procesados correctamente.")