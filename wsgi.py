import sys
import os

# Añade la carpeta del proyecto al PATH del sistema
sys.path.insert(0, os.path.dirname(__file__))

# Importa la instancia de la aplicación Flask desde app.py
from app import app as application

