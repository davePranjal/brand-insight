import os
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from src.api_layer.api import app as fastapi_app  # Import your FastAPI app instance
from config import Settings
# from src.database import Database

load_dotenv()  # Load environment variables from .env file

# Load configuration settings
settings = Settings()


# # Register the OpenAI client as a dependency for FastAPI
# fastapi_app.dependency_overrides[OpenAIClient] = lambda: openai_client
# fastapi_app.dependency_overrides[Database] = lambda: database

# Check for required environment variables
required_env_vars = ["OPENAI_API_KEY", "MONGO_DB_URL"]  # Add more as needed
for var in required_env_vars:
    if var not in os.environ:
        raise EnvironmentError(f"Missing required environment variable: {var}")

# Main function to run the server
if __name__ == "__main__":
    uvicorn.run(
        "src.api_layer.api:app",  # Assuming your FastAPI app instance is named 'app'
        host=settings.host,
        port=settings.port,
        reload=settings.reload,  # Reload on code changes if in debug mode
    )
