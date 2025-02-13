if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
from mage_ai.io.snowflake import Snowflake
import os

@data_loader
def load_data(dataframes, *args, **kwargs):
    """
    Carga los DataFrames en Snowflake.
    """
    with Snowflake(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
    ) as db:
        
        for table, df in dataframes.items():
            print(f"Cargando {len(df)} filas en la tabla '{table}'...")
            db.export(df, table, if_exists="replace")  # "replace" borra y recrea la tabla
            print(f"✅ Carga completa para '{table}'.")

    return dataframes

@test
def test_output(output, *args) -> None:
    assert output is not None, 'La carga falló, no hay datos'
    assert len(output) > 0, 'El dataframe está vacío'