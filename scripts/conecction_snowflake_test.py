from mage_ai.io.snowflake import Snowflake
import os

try:
    db = Snowflake(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
    )

    db.open()
    df = db.load("SELECT current_version()")
    print("Conexión exitosa a Snowflake. Versión:", df.iloc[0, 0])
    db.close()
except Exception as e:
    print("Error al conectar a Snowflake:", e)