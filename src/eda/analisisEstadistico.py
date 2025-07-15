# src/eda/procesador_eda.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class ProcesadorEDA:
    def __init__(self, df):
        self.df = df

    def limpieza_datos(self):
        self.df.dropna(inplace=True)
        self.df['fecha'] = pd.to_datetime(self.df['fecha'])
        return self.df

    def resumen_descriptivo(self):
        return self.df.describe(include='all')

    def matriz_correlacion(self):
        corr = self.df.corr(numeric_only=True)
        sns.heatmap(corr, annot=True)
        plt.title("Matriz de Correlación")
        plt.show()