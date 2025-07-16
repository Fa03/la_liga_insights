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

    def tabla_posiciones(self):
        equipos = pd.concat([self.df['equipo_local'], self.df['equipo_visita']]).unique()
        tabla = pd.DataFrame(index=equipos, columns=['PJ', 'PG', 'PE', 'PP', 'GF', 'GC', 'DG', 'Pts']).fillna(0)

        for _, row in self.df.iterrows():
            local = row['equipo_local']
            visita = row['equipo_visita']
            gl = row['goles_local']
            gv = row['goles_visita']

            tabla.loc[local, 'PJ'] += 1
            tabla.loc[visita, 'PJ'] += 1

            tabla.loc[local, 'GF'] += gl
            tabla.loc[local, 'GC'] += gv
            tabla.loc[visita, 'GF'] += gv
            tabla.loc[visita, 'GC'] += gl

            if gl > gv:
                tabla.loc[local, 'PG'] += 1
                tabla.loc[visita, 'PP'] += 1
            elif gl < gv:
                tabla.loc[visita, 'PG'] += 1
                tabla.loc[local, 'PP'] += 1
            else:
                tabla.loc[local, 'PE'] += 1
                tabla.loc[visita, 'PE'] += 1

        tabla['DG'] = tabla['GF'] - tabla['GC']
        tabla['Pts'] = tabla['PG'] * 3 + tabla['PE']
        tabla = tabla.sort_values(by=['Pts', 'DG', 'GF'], ascending=False).reset_index().rename(
            columns={'index': 'equipo'})
        return tabla

    def tarjetas_faltas(self):
        tarjetas = self.df.groupby(['equipo_local']).agg({
            'amarillas_local': 'sum',
            'rojas_local': 'sum',
            'faltas_local': 'sum'
        }).add(
            self.df.groupby(['equipo_visita']).agg({
                'amarillas_visita': 'sum',
                'rojas_visita': 'sum',
                'faltas_visita': 'sum'
            }), fill_value=0
        ).reset_index().rename(columns={'equipo_local': 'equipo'})

        return tarjetas