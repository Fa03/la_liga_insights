import pandas as pd
import numpy as np


class ProcesadorEDA:
    def __init__(self, df):
        self.df = df

    # Devuelve un resumen estadístico de las columnas numéricas de la tabla
    def resumen_descriptivo(self):
        print("📊 Resumen descriptivo:")
        return self.df.describe()  # describe() calcula media, std, percentiles, etc.

    def matriz_correlacion(self, metodo='pearson'):
        """
        Calcula la matriz de correlación y la devuelve como DataFrame.
        """
        df_numerico = self.df.select_dtypes(include='number')
        corr = df_numerico.corr(method=metodo)
        return corr

    def distribucion_variable(self, columna, bins=5):
        """
        Calcula la distribución de frecuencias para una columna.
        Devuelve un DataFrame con intervalos y conteo.
        """
        df = self.df
        series = df[columna].dropna()
        counts, bin_edges = np.histogram(series, bins=bins)
        df_hist = pd.DataFrame({
            'intervalo': pd.IntervalIndex.from_arrays(bin_edges[:-1], bin_edges[1:]),
            'conteo': counts
        })
        return df_hist

    # Detecta outliers en una columna usando el método de Z-score
    def detectar_outliers(self, columna, z_threshold=3):
        df = self.df
        if columna not in df.columns:
            raise ValueError(f"La columna {columna} no existe.")

        # calcula media y desviación estándar
        mean = df[columna].mean()
        std = df[columna].std()

        # calcula el Z-score para cada valor
        z_scores = (df[columna] - mean) / std

        # filtra los valores cuyo |z| > umbral
        outliers = df[np.abs(z_scores) > z_threshold]

        print(f"🚨 Outliers detectados en {columna}:")
        return outliers

    def conteo_outliers(self, columnas=None, z_threshold=3):
        """
        Devuelve un Series con la cantidad de outliers por variable.
        """
        df = self.df
        if columnas is None:
            columnas = df.select_dtypes(include='number').columns

        outliers_count = {}
        for col in columnas:
            z = np.abs((df[col] - df[col].mean()) / df[col].std())
            outliers_count[col] = (z > z_threshold).sum()

        return pd.Series(outliers_count).sort_values(ascending=False)

#====================================

    