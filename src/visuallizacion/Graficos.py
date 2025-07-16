import matplotlib.pyplot as plt
import seaborn as sns


class Visualizador:
    def __init__(self, eda):
        """
        Inicializa el visualizador con objetos de ProcesadorEDA y EstadisticasFutbol
        """
        self.eda = eda

    def graficar_matriz_correlacion(self):
        """
        Obtiene el DataFrame de correlaciones y lo grafica como heatmap.
        """
        corr_df = self.eda.matriz_correlacion()
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_df, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('Matriz de Correlación')
        plt.show()

    def graficar_distribucion_variable(self, columna):
        """
        Obtiene el DataFrame con distribución de frecuencias y la grafica como histograma.
        Muestra el valor exacto de cada barra en la parte superior.
        """
        df_hist = self.eda.distribucion_variable(columna)
        plt.figure(figsize=(10, 6))

        # Convertimos los intervalos a string para usarlos como etiquetas
        x_labels = df_hist['intervalo'].astype(str)
        conteos = df_hist['conteo']

        # Graficar barras
        bars = plt.bar(x_labels, conteos, color='skyblue', edgecolor='black')

        # Añadir los valores encima de cada barra
        for bar in bars:
            altura = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, altura + 0.5, str(altura),
                     ha='center', va='bottom', fontsize=10, fontweight='bold')

        plt.xticks(rotation=90)
        plt.title(f'Distribución de {columna}')
        plt.xlabel('Intervalo')
        plt.ylabel('Frecuencia')
        plt.tight_layout()
        plt.show()

    def distribucion_outliers(self):
        """
        Barras con conteo de outliers por variable.
        Historia: ¿Qué variable tiene más valores atípicos?
        """
        series_outliers = self.eda.conteo_outliers()
        series_outliers.sort_values().plot(kind='barh', figsize=(8, 6), color='red')
        plt.title('Outliers detectados por variable')
        plt.xlabel('Cantidad de Outliers')
        plt.ylabel('Variable')
        plt.show()

    def histograma_goles_por_partido(self):
        """
        Histograma de goles a favor por equipo.
        Historia: ¿Qué tan ofensivos son los equipos? ¿Hay alguno muy superior al resto?
        """
        df_posiciones = self.eda.tabla_posiciones()
        plt.figure(figsize=(10, 6))
        sns.histplot(df_posiciones['GF'], bins=10, kde=True, color='blue')
        plt.title('Distribución de Goles a Favor por Equipo')
        plt.xlabel('Goles a favor')
        plt.ylabel('Número de equipos')
        plt.show()

    def goles_vs_puntos(self):
        """
        Dispersión entre goles a favor y puntos totales.
        Historia: ¿Convierte goles en puntos o desperdicia su ofensiva?
        """
        df_posiciones = self.eda.tabla_posiciones()
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='GF', y='Pts', data=df_posiciones, hue='equipo', s=100)
        plt.title('Relación entre Goles a Favor y Puntos Obtenidos')
        plt.xlabel('Goles a favor')
        plt.ylabel('Puntos')
        plt.show()

    def top_n_equipos(self, n=5):
        """
        Barras horizontales con los mejores equipos según puntos.
        Historia: ¿Quiénes dominan la tabla? ¿Cuál es la diferencia?
        """
        df_posiciones = self.eda.tabla_posiciones()
        top_n = df_posiciones.sort_values(by='Pts', ascending=False).head(n)
        plt.figure(figsize=(8, 5))
        sns.barplot(x='Pts', y='equipo', data=top_n, palette='viridis')
        plt.title(f'Top {n} Equipos por Puntos')
        plt.xlabel('Puntos')
        plt.ylabel('Equipo')
        plt.show()

    def scatter_efectividad_tiros(self, df_tiros):
        """
        Dispersión entre % a puerta y % de goles por tiro.
        Historia: ¿Qué equipos son más precisos? ¿Hay alguno que genera mucho pero convierte poco?
        """
        fig = px.scatter(
            df_tiros,
            x='porcentaje_a_puerta',
            y='porcentaje_goles_por_tiro',
            size='tiros',
            color='equipo',
            text='equipo',
            title='Efectividad de Tiros: precisión vs conversión'
        )
        fig.update_traces(textposition='top center')
        fig.show()

    def barras_tarjetas_faltas(self, df_tarjetas):
        """
        Barras comparando amarillas, rojas y faltas.
        Historia: ¿Qué equipo es más agresivo? ¿Hay uno que combine muchas faltas y muchas rojas?
        """
        df_tarjetas.set_index('equipo')[['amarillas', 'rojas', 'faltas']].plot(
            kind='bar', figsize=(12, 6), colormap='Set2'
        )
        plt.title('Tarjetas y Faltas por Equipo')
        plt.ylabel('Cantidad')
        plt.show()


