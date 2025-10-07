from dotenv import load_dotenv

from core.setup import create_app

load_dotenv(".env")

app = create_app()







