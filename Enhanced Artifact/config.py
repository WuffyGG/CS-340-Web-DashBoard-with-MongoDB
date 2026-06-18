import os

DB_USER = os.getenv("DB_USER", "aacuser")
DB_PASS = os.getenv("DB_PASS", "SNHU1234")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "27017"))
DB_NAME = os.getenv("DB_NAME", "aac")
DB_COLLECTION = os.getenv("DB_COLLECTION", "animals")

APP_PORT = int(os.getenv("APP_PORT", "8053"))
LOGO_FILE = os.getenv("LOGO_FILE", "Grazioso Salvare Logo.png")