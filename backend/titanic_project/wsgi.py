"""
WSGI config for titanic_project project.
"""

import os
import sys                 # <--- 1. AÑADE ESTA LÍNEA
from pathlib import Path    # <--- 2. AÑADE ESTA LÍNEA

from django.core.wsgi import get_wsgi_application

# --- 3. AÑADE ESTAS DOS LÍNEAS ---
# (La ruta aquí necesita .parent tres veces para llegar a la raíz)
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
# ----------------------------------

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.titanic_project.settings')

application = get_wsgi_application()