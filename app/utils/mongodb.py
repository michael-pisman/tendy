"""
Module for initializing MongoDB connection and configuring Beanie ODM.

This module sets up the connection to the MongoDB database using Motor and initializes
Beanie with the application's document models.
"""

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from devtools import pprint

from app.config import get_config
# from app.documents import DOCUMENTS

# Retrieve application settings which include MongoDB connection details.
CONFIG = get_config()

class MongoDB:
    client: AsyncIOMotorClient
    db: AsyncIOMotorDatabase

    @classmethod
    async def init(cls, mongo_uri: str = CONFIG.mongo_uri, db_name: str = CONFIG.mongo_dbname) -> None:
        """
        Initialize the MongoDB connection and configure Beanie ODM.

        This function creates a Motor client using the MongoDB URL from the settings,
        selects the database specified in settings, and initializes Beanie with the document
        models. It should be called during application startup.

        Raises:
            Exception: If unable to connect to MongoDB or initialize Beanie.
        """
        
        # Create a Motor client to interact with MongoDB.
        cls.client = AsyncIOMotorClient(mongo_uri, connect=True)

        # Access the database using the name provided in the settings.
        cls.db = cls.client.get_database(db_name)

        # Initialize Beanie with the database and the list of document models.
        await init_beanie(database=cls.db, document_models=[])  # type: ignore


    @classmethod
    async def close(cls) -> None:
        """
        Close the MongoDB connection.

        This function closes the MongoDB connection when the application is shutting down.
        """
        cls.client.close()

    @classmethod
    async def get_client(cls) -> AsyncIOMotorClient:
        """
        Get the MongoDB client.

        This function returns the MongoDB client instance. It can be used to interact
        with the database directly if needed.

        Returns:
            AsyncIOMotorClient: The MongoDB client instance.
        """
        return cls.client

    @classmethod
    async def get_database(cls) -> AsyncIOMotorDatabase:
        """
        Get the MongoDB database.

        This function returns the MongoDB database instance. It can be used to interact
        with the database directly if needed.

        Returns:
            AsyncIOMotorDatabase: The MongoDB database instance.
        """
        return cls.db
    
    # @classmethod
    # async def drop_database(cls) -> None:
    #     """
    #     Drop the MongoDB database.

    #     This function drops the database specified in the application settings.
    #     It should only be used in a testing environment.

    #     Raises:
    #         Exception: If unable to drop the database.
    #     """
    #     client = await cls.get_client()
    #     await client.drop_database(CONFIG.mongo_dbname)

    @classmethod
    async def test_connection(cls) -> bool:
        """
        Test the MongoDB connection.

        This function attempts to retrieve the database instance to verify the connection.
        """
        db = await cls.get_database()
        try: 
            response = await db.command("ping")
            assert response.get("ok") == 1
            return True
        except Exception as e:
            print("Could not connect to MongoDB, check your connection settings:")
            pprint(e)
        return False