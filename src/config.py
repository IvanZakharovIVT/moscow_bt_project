import json
import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')

DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}'
DATABASE_A_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}'

MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')
MINIO_ADDRESS = os.getenv('MINIO_ADDRESS')
MINIO_IS_SECURE = (os.getenv('MINIO_IS_SECURE', 'False').capitalize() == 'True')

SPECIAL_SYMBOLS_TEMPLATE = r"[^a-zA-Z0-9_\s]+"

ORIGINS = json.loads(os.getenv("ORIGINS", '["*"]'))

BASE_ML_API_URL = os.getenv('BASE_ML_API_URL', '')

PROJECT_DIR = Path.cwd()
TEMPLATE_FILE_PATH = PROJECT_DIR / os.getenv("TEMPLATE_FILE_PATH", 'media_files/templates/')
BUFFER_FILE_PATH = PROJECT_DIR / os.getenv("BUFFER_FILE_PATH", 'media_files/buffer_files/')

INVOICE_TEMPLATE = TEMPLATE_FILE_PATH / "invoice_template.docx"
CONTRACT_TEMPLATE = TEMPLATE_FILE_PATH / "contract_template.docx"

DEBUG = os.getenv('DEBUG', True)

DEFAULT_ADMIN_USERNAME = os.getenv('DEFAULT_ADMIN_USERNAME')
DEFAULT_ADMIN_PASSWORD = os.getenv('DEFAULT_ADMIN_PASSWORD')
