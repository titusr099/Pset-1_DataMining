if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
from mage_ai.io.mysql import MySQL
import os

@data_loader
def load_data(*args, **kwargs):
    """
    Extrae todas las tablas de la base de datos MySQL y las devuelve en un diccionario de DataFrames.
    """
    with MySQL(
        database=os.getenv("MYSQL_DATABASE"),
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        port=int(os.getenv("MYSQL_PORT")),
    ) as db:
        
        # Obtener nombres de todas las tablas
        cursor = db.conn.cursor()
        cursor.execute("SHOW TABLES;")
        table_names = [row[0] for row in cursor.fetchall()]
        cursor.close()

        print(f"Tablas encontradas: {table_names}")

        # Extraer datos de cada tabla y guardarlos en un diccionario
        dataframes = {}
        for table in table_names:
            query = f"SELECT * FROM {table};" 
            dataframes[table] = db.load(query)
            print(f"✅ Tabla '{table}' extraída con {len(dataframes[table])} filas.")

    return dataframes  # Retorna un diccionario con DataFrames

@test
def test_output(output, *args) -> None:
    """
    Prueba que al menos una tabla fue extraída correctamente.
    """
    assert output is not None, "No se extrajo ninguna tabla."
    assert isinstance(output, dict), "El resultado debe ser un diccionario de DataFrames."
    assert len(output) > 0, "No hay tablas extraídas."
    for table, df in output.items():
        assert len(df) > 0, f"La tabla {table} está vacía."