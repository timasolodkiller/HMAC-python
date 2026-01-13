"""Main module for run FastAPI application"""

import uvicorn

from src.app import app
from src.config import SETTINGS

if __name__ == '__main__':
    host = SETTINGS.host
    port = SETTINGS.port
    uvicorn.run(app, host=host, port=port)
