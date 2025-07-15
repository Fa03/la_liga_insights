import sys
import os
sys.path.append(os.path.abspath("C:/Users/fab_t/OneDrive/CUC/PrograII/la_liga_insights/src/basedatos/"))

from GestorBaseDatos import CargaDatos

# Creación de objeto
gestionBD = CargaDatos('AZUSFA\\FA_LOCALSERVER', 'La_Liga_Insights', 'C:/Users/fab_t/OneDrive/CUC/PrograII/la_liga_insights/data/partidos-laliga-2024-2025.csv', ['partidos'])

# Invocación de metodo para conexión

gestionBD.conectar()

# gestionBD.insertar_datos()  Comentado por que ya si hizo la inserción de datos!