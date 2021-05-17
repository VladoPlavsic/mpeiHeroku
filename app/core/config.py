from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

PROJECT_NAME = "hope"
VERSION = "1.0.0"
API_PREFIX = "/api"

# EMAIL
SERVER_EMAIL = config("SERVER_EMAIL", cast=str,  default="vladoplavsicvladoplavsic@gmail.com")
ADMIN_EMAIL = config("ADMIN_EMAIL", cast=str, default='johnyglup98@gmail.com')
# GMAIL
GMAIL_TOKEN = config("GMAIL_TOKEN", cast=str)
GMAIL_REFRESH_TOKEN = config("GMAIL_REFRESH_TOKEN", cast=str)
GMAIL_TOKEN_URI = config("GMAIL_TOKEN_URI", cast=str)
GMAIL_CLIENT_ID = config("GMAIL_CLIENT_ID", cast=str)
GMAIL_CLIENT_SECRET = config("GMAIL_CLIENT_SECRET", cast=Secret)

# CDN CREDS
AWS_SECRET_KEY_ID = config("AWS_SECRET_KEY_ID", cast=str)
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", cast=str)
CDN_ENDPOINT_URL = config("CDN_ENDPOINT_URL", cast=str)

# CDN SETTINGS
BUCKET = config("BUCKET", cast=str, default="mpei")
CDN_LINK_LIFESPAN = config("CDN_LINK_LIFESPAN_SECONDS", cast=int, default=7 * 24 * 60 * 60) # age in seconds NOTE: Max alowed 7 days

# SERVER CREDS AND SETTINGS
SECRET_KEY = config("SECRET_KEY", cast=Secret)
ACCESS_TOKEN_EXPIRE_MINUTES = config(
  "ACCESS_TOKEN_EXPIRE_MINUTES",
  cast=int,
  default=7 * 24 * 60 #one week
)
JWT_ALGORITHM = config("JWT_ALGORITHM", cast=str, default="HS256")
JWT_AUDIENCE = config("JWT_AUDIENCE", cast=str, default="mpei-kids:auth")
JWT_TOKEN_PREFIX = config("JWT_TOKEN_PREFIX", cast=str, default="Bearer")

# POSTGRES
POSTGRES_USER = config("POSTGRES_USER", cast=str)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str, default="db")
POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="5432")
POSTGRES_DB = config("POSTGRES_DB", cast=str)

DATABASE_URL = config(
  "DATABASE_URL",
  cast=DatabaseURL,
  default=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# SITE URL
SITE_URL = config("SITE_URL", cast=str, default="http://localhost:8080")