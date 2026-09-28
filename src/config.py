import os
from pathlib import Path

from dotenv import load_dotenv


# ============================================================
# RUTAS DEL PROYECTO
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

WORKSPACE_DIR = BASE_DIR / "workspace"
MEMORY_DIR = BASE_DIR / "memory"


# Crear directorios si no existen
WORKSPACE_DIR.mkdir(exist_ok=True)
MEMORY_DIR.mkdir(exist_ok=True)


# ============================================================
# VARIABLES DE ENTORNO
# ============================================================

ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


# ============================================================
# CONFIGURACIÓN DE LA IA
# ============================================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-5.6"
)


# ============================================================
# CONFIGURACIÓN DE FLOWNEXUS
# ============================================================

FLOWNEXUS_NAME = os.getenv(
    "FLOWNEXUS_NAME",
    "FlowNexus"
)

FLOWNEXUS_ENV = os.getenv(
    "FLOWNEXUS_ENV",
    "development"
)


# ============================================================
# CONFIGURACIÓN DE INVESTIGACIÓN
# ============================================================

MAX_SEARCH_RESULTS = int(
    os.getenv(
        "MAX_SEARCH_RESULTS",
        "5"
    )
)

REQUEST_TIMEOUT = int(
    os.getenv(
        "REQUEST_TIMEOUT",
        "15"
    )
)


# ============================================================
# ARCHIVOS DE MEMORIA
# ============================================================

MEMORY_FILE = MEMORY_DIR / "conversation.json"


# ============================================================
# VALIDACIÓN
# ============================================================

def validate_config():
    """
    Comprueba que la configuración mínima
    de FlowNexus esté disponible.
    """

    if not OPENAI_API_KEY:
        raise ValueError(
            "No se encontró OPENAI_API_KEY. "
            "Configúrala en el archivo .env"
        )

    if not OPENAI_MODEL:
        raise ValueError(
            "No se ha configurado OPENAI_MODEL."
        )


# ============================================================
# INFORMACIÓN DE CONFIGURACIÓN
# ============================================================

def show_config():
    """
    Muestra información básica de configuración
    sin revelar claves privadas.
    """

    print("=" * 50)
    print(f"{FLOWNEXUS_NAME}")
    print("=" * 50)

    print(f"Entorno: {FLOWNEXUS_ENV}")
    print(f"Modelo: {OPENAI_MODEL}")
    print(f"Workspace: {WORKSPACE_DIR}")
    print(f"Memoria: {MEMORY_DIR}")

    if OPENAI_API_KEY:
        print("API Key: configurada")
    else:
        print("API Key: NO configurada")

    print("=" * 50)
