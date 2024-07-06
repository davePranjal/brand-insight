import os
import uvicorn
from dotenv import load_dotenv
from config import Settings

load_dotenv()  # Load environment variables from .env file

# Load configuration settings
settings = Settings()


# Check for required environment variables
required_env_vars = ["OPENAI_API_KEY", "MONGO_DB_URL", "OPENAI_MODEL"]
for var in required_env_vars:
    if var not in os.environ:
        raise EnvironmentError(f"Missing required environment variable: {var}")

# Main function to run the server
if __name__ == "__main__":
    uvicorn.run(
        "src.api_layer.api:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
    )
