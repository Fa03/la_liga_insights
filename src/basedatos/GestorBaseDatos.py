import pandas as pd
import pyodbc
import os
import unicodedata

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

    @staticmethod
    def normalizar_nombre_columna(nombre):
        normalizado = unicodedata.normalize('NFKD', nombre).encode('ASCII', 'ignore').decode('ASCII')
        return normalizado.replace(' ', '_').lower()

    def insertar_datos(self):
        for tabla in self.tablas:
            archivo = os.path.join(self.ruta_csv, f'{tabla}.csv')
            if not os.path.exists(archivo):
                print(f"⚠️ Archivo no encontrado: {archivo}")
                continue

            df = pd.read_csv(archivo, encoding='utf-8-sig')
            df.columns = [self.normalizar_nombre_columna(col) for col in df.columns]
            columnas = df.columns.tolist()
            placeholders = ', '.join(['?'] * len(columnas))
            columnas_sql = ', '.join(columnas)

            print(f"📥 Insertando datos en la tabla: {tabla} ({len(df)} filas)")

            for _, fila in df.iterrows():
                valores = [fila[col] for col in columnas]
                try:
                    self.cursor.execute(
                        f"INSERT INTO {tabla} ({columnas_sql}) VALUES ({placeholders})",
                        valores
                    )
                except pyodbc.Error as e:
                    print(f"❌ Error insertando fila en {tabla}: {e}")
                    continue

            self.conn.commit()
            print(f"✅ Datos insertados en {tabla}")

# Ejemplo de uso
if __name__ == "__main__":
    tablas = [
        'estadisticas_jugadores',
        'estadisticas_partidos',
        'evolucion_equipos',
        'goles_por_partido',
        'jugadores_top',
        'lesiones_jugadores'
    ]
    cargador = CargaDatos('AzusFa\\SQLEXPRESS', 'CopaOro', 'copa_oro_datos', tablas)
    cargador.conectar()
    cargador.insertar_datos()
    cargador.cerrar_conexion()
