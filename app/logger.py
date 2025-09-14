# app/logger.py
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),  # log to stdout (good for Docker)
        logging.FileHandler("app.log", mode="a"),  # also log to file
    ]
)

# Get a logger for the app
logger = logging.getLogger("fastapi_assignment")
