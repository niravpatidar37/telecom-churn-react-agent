import uvicorn
import logging
from src.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info(f"Starting Telecom Churn Agent on {settings.HOST}:{settings.PORT}")
    uvicorn.run("src.api:app", host=settings.HOST, port=settings.PORT, reload=True)
