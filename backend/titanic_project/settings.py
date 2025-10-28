import os
from pathlib import Path
from dotenv import load_dotenv  # <-- Añade esto

# Cargar variables de entorno
load_dotenv()  # <-- Añade esto

BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración más flexible
SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-temporal-para-desarrollo')
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = [
    '127.0.0.1', 
    'localhost', 
    '.localhost',
    'prediccion-titanic-vl0y.onrender.com', # <--- AÑADE ESTA LÍNEA
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'backend.predictor', # no hay coma extra
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Mantener pero configurar
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --- AÑADE ESTA LÍNEA ---
ROOT_URLCONF = 'backend.titanic_project.urls'
# ------------------------

# ... (el resto de configuraciones se mantienen igual)

# Añadí la línea que faltaba: ROOT_URLCONF = 'backend.titanic_project.urls'
# Por favor, asegúrate de que esta línea esté presente en tu archivo settings.py.

TEMPLATES = [ # Asegúrate de tener esta sección también
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.titanic_project.wsgi.application' # Verifica que esta línea también esté correcta

# Static files - configuración para desarrollo
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Configuración de WhiteNoise solo en producción
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
else:
    # En desarrollo, servir archivos estáticos normalmente
    # STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] # Comenté esto temporalmente, podría dar error si no existe la carpeta
    STATICFILES_DIRS = []


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Configuración de CORS
CORS_ALLOW_ALL_ORIGINS = True # Para desarrollo está bien, en producción considera ser más específico
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000", # Añadí este por si acaso
]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Password validation - Asegúrate de tener esto también
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# Internationalization - Asegúrate de tener esto también
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True