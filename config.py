# to load database url

import os #access system .env
from dotenv import load_dotenv #load .env content into environment variables

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


