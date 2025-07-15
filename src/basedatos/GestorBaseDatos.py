import pandas as pd
import pyodbc
import os
import unicodedata
import numpy as np

class CargaDatos:
    def __init__(self, server, database, ruta_csv, tablas):
        self.server = server
        self.database = database
        self.ruta_csv = ruta_csv
        self.tablas = tablas
        self.conn = None
        self.cursor = None

    def conectar(self):
        self.conn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;'
        )
        self.cursor = self.conn.cursor()
        print("✅ Conexión establecida")

    def cerrar_conexion(self):
        if self.cursor: self.cursor.close()
        if self.conn: self.conn.close()
        print("🔒 Conexión cerrada")

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

            # Read CSV with proper numeric handling
            df = pd.read_csv(archivo, encoding='utf-8-sig', sep=',', decimal='.')
            
            # Convert empty strings to None and handle numeric conversions
            df = df.replace(['', 'NULL', 'null'], np.nan)
            
            columnas = df.columns.tolist()
            placeholders = ', '.join(['?'] * len(columnas))
            columnas_sql = ', '.join(columnas)

            print(f"📥 Insertando datos en la tabla: {tabla} ({len(df)} filas)")

            for _, fila in df.iterrows():
                # Limpiar y convertir valores
                valores = [self.convertirValoresNulos(fila[col]) for col in columnas]
                try:
                    self.cursor.execute(
                        f"INSERT INTO {tabla} ({columnas_sql}) VALUES ({placeholders})",
                        valores
                    )
                except pyodbc.Error as e:
                    print(f"❌ Error insertando fila en {tabla}: {e}")
                    print(f"Valores problemáticos: {valores}")
                    continue

            self.conn.commit()
            print(f"✅ Datos insertados en {tabla}")