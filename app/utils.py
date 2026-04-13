import os
import sys

def ruta_recurso(ruta_relativa):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, ruta_relativa)