from fastapi import Header, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
import os
from .logger import logger  # ✅ your logger

# -----------------------------
# API key setup
# -----------------------------
API_KEY = os.getenv("API_KEY", "StantechAI")
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


# -----------------------------
# API key validation
# -----------------------------
async def get_api_key(api_key: str = Security(api_key_header)):
    if not api_key:
        logger.warning("API Key missing in request")
        raise HTTPException(status_code=401, detail="API Key missing")
    
    if api_key != API_KEY:
        logger.warning(f"Invalid API Key attempted: {api_key}")
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    logger.info(f"✅ API Key validated successfully: {api_key}")
    return api_key
