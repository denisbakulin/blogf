from dotenv import load_dotenv

from base.setup import create_app
from pathlib import Path


env_path = Path(__file__).parent.parent
load_dotenv(env_path / ".env")

app = create_app()







