import pandas as pd
import pyodbc
import os
import unicodedata
import numpy as np
from sqlalchemy import create_engine, text

class CargaDatos:
    def __init__(self, server, database, ruta_csv, tablas):
        self.server = server
        self.database = database
        self.ruta_csv = ruta_csv
        self.tablas = tablas
        self.conn = None
        self.engine = None

    def conectar(self):
        connection_string = (
            f"mssql+pyodbc://@{self.server}/{self.database}"
            "?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
        )
        self.engine = create_engine(connection_string, fast_executemany=True)
        self.conn = self.engine.connect()
        print("✅ Conexión establecida con SQLAlchemy")

        # Cierra la conexión y libera recursos
    def cerrar_conexion(self):
        if self.conn:
            self.conn.close()
            print("🔒 Conexión cerrada")
        if self.engine:
            self.engine.dispose()

#metodo necesario para manejar nulos en datos de origen vs tipo de dato destino
    def convertirValoresNulos(self, value):
        if pd.isna(value) or value == '':
            return None
        if isinstance(value, (int, float)):
            return float(value) if isinstance(value, int) else value
        if isinstance(value, str):
            # Try to convert string to float if possible
            try:
                return float(value.replace(',', '.'))
            except (ValueError, TypeError):
                return value
        return value

    def insertar_datos(self):
        for tabla in self.tablas:
            archivo = self.ruta_csv
            if not os.path.exists(archivo):
                print(f"⚠️ Archivo no encontrado: {archivo}")
                continue

            df = pd.read_csv(archivo, encoding='utf-8-sig', sep=',', decimal='.')
            df = df.replace(['', 'NULL', 'null'], np.nan)

            columnas = df.columns.tolist()
            columnas_sql = ', '.join(columnas)
            placeholders = ', '.join([f":{col}" for col in columnas])  # SQLAlchemy style

            print(f"📥 Insertando datos en la tabla: {tabla} ({len(df)} filas)")

            with self.engine.begin() as connection:  # Usa begin() para manejar transacciones automáticamente
                for _, fila in df.iterrows():
                    valores = {col: self.convertirValoresNulos(fila[col]) for col in columnas}
                    try:
                        statement = text(f"INSERT INTO {tabla} ({columnas_sql}) VALUES ({placeholders})")
                        connection.execute(statement, valores)
                    except Exception as e:
                        print(f"❌ Error insertando fila en {tabla}: {e}")
                        print(f"Valores problemáticos: {valores}")
                        continue

            print(f"✅ Datos insertados en {tabla}")

            # ============================================
    def get_tabla(self):
        return self.tablas[0]

    def get_conn(self):
        return self.conn

    def cargar_datos(self):
        query = f"SELECT * FROM {self.tablas[0]}"
        df = pd.read_sql(query, self.conn)
        print(f"📥 Datos cargados: {df.shape[0]} filas, {df.shape[1]} columnas")
        return df


    def get_partido(self, id_partido):
        query = text(f"SELECT * FROM {self.tablas[0]} WHERE id_partido = :id")
        df = pd.read_sql(query, self.conn, params={"id": id_partido})
        return df

    def get_por_equipo(self, equipo):
        query = text(f"""
            SELECT * FROM {self.tablas[0]}
            WHERE equipo_local = :eq OR equipo_visita = :eq
        """)
        df = pd.read_sql(query, self.conn, params={"eq": equipo})
        return df

    def get_por_temporada(self, temporada):
        query = text(f"SELECT * FROM {self.tablas[0]} WHERE temporada = :temp")
        df = pd.read_sql(query, self.conn, params={"temp": temporada})
        return df

    def home_advantage(self):
        query = f"""
            SELECT
                SUM(CASE WHEN goles_local > goles_visita THEN 1 ELSE 0 END) AS victorias_local,
                SUM(CASE WHEN goles_local < goles_visita THEN 1 ELSE 0 END) AS victorias_visita,
                SUM(CASE WHEN goles_local = goles_visita THEN 1 ELSE 0 END) AS empates
            FROM {self.tablas[0]}
        """
        df = pd.read_sql(query, self.conn)
        # return df.iloc[0].to_dict() # para mostrar en forma de diccionario
        return df # se muestra el Data Frame