"""
This is the main application file for the FastAPI application.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

# from app.api import router
from app.config import get_config
from app.utils.mongodb import MongoDB
from app.api import router as api_router

# Load application settings from environment or configuration.
CONFIG = get_config()

mongodb = MongoDB()


# Function to run on application startup.
async def startup() -> None:
    """
    Startup function to initialize the application.
    """
    await mongodb.init()  # Initialize MongoDB connection


# Function run on application shutdown.
async def shutdown() -> None:
    """
    Shutdown function to clean up resources.
    """
    await mongodb.close()  # Close MongoDB connection when the application shuts down


# Lifespan context manager for FastAPI application.
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Application lifespan context manager for FastAPI.

    This context manager handles startup and shutdown events for the application.
    On startup, it connects to MongoDB by calling init_mongo().
    On shutdown, any required cleanup logic (e.g., closing database connections)
    can be added here.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: Control is yielded back after startup actions.
    """
    await startup()  # Connect to MongoDB during app startup
    yield  # Yield control back to the application
    await shutdown()  # Perform cleanup actions on app shutdown


# Create a FastAPI application instance, using the custom lifespan context manager.
app = FastAPI(title="MyPyProject",
              lifespan=lifespan)
app.include_router(api_router)


