import sys
import os

# Para invocar clases guardadas en otra carpetas
sys.path.append(os.path.abspath("C:/Users/fab_t/OneDrive/CUC/PrograII/la_liga_insights/src/basedatos/"))
from GestorBaseDatos import CargaDatos

sys.path.append(os.path.abspath("C:/Users/fab_t/OneDrive/CUC/PrograII/la_liga_insights/src/eda/"))
from analisisEstadistico import ProcesadorEDA

sys.path.append(os.path.abspath("C:/Users/fab_t/OneDrive/CUC/PrograII/la_liga_insights/src/visuallizacion/"))
from Graficos import Visualizador


# Creación de objeto de la clase CargaDatos
gestionBD = CargaDatos('AZUSFA\\FA_LOCALSERVER', 'La_Liga_Insights', 'C:/Users/fab_t/OneDrive/CUC/PrograII/la_liga_insights/data/partidos-laliga-2024-2025.csv', ['partidos'])

# Invocación de metodo para conexión

gestionBD.conectar()

# gestionBD.insertar_datos()  Comentado por que ya si hizo la inserción de datos!

# ====================================

print(gestionBD.get_partido(123))
print(gestionBD.get_por_equipo("Barcelona"))
print(gestionBD.get_por_temporada(2024))
print(gestionBD.home_advantage())

# Verificación  Clase Estadística

## Creación de objeto para clase procesadorEDA

df_ParaAnalisis = gestionBD.cargar_datos() # metodo está en el modulo GestorBaseDatos
estadistica = ProcesadorEDA(df_ParaAnalisis)
print(estadistica.resumen_descriptivo())

## Matriz de Corelacion
print("Se muensta la correlación entre variable \n",estadistica.matriz_correlacion())

## Distribución Variable (extra)
print(estadistica.distribucion_variable('goles_visita'))

## Outliers (datos atípicos)
print(estadistica.detectar_outliers('goles_local'))

## Para ver la tabla de posiciones para gráfico
print('Este es el dataframe de tabla posiciones \n',estadistica.tabla_posiciones())

## Para ver DF que se genera para gráfico de tarjetas
print('Tabla d?\n',estadistica.tarjetas_faltas())

# Graficación

## Objeto de la clase Visualizador para mostrar los gráficos
graficos = Visualizador(estadistica)

## Primer Gráfico
graficos.graficar_matriz_correlacion()

## Segundo Gráfico
graficos.graficar_distribucion_variable('goles_visita')

## Tercer Gráfico
graficos.distribucion_outliers()

## Cuato Gráfico
graficos.histograma_goles_por_partido()

## Quinto Gráfico
graficos.top_n_equipos()

## Sexto Gráfico
graficos.barras_tarjetas_faltas()






