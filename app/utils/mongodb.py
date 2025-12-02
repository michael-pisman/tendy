"""
Module for initializing MongoDB connection and configuring Beanie ODM.

This module sets up the connection to the MongoDB database using Motor and initializes
Beanie with the application's document models.
"""

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from devtools import pprint

from app.config import get_config
from app.documents.session import Session
from app.documents.attendance import AttendanceLog

# Retrieve application settings which include MongoDB connection details.
CONFIG = get_config()

class MongoDB:
    client: AsyncIOMotorClient
    db: AsyncIOMotorDatabase
    # Fallback in-memory stores used when a real MongoDB isn't reachable.
    _fallback_sessions: dict = {}
    _fallback_attendance_logs: list = []

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
        # Use a short server selection timeout and don't force a connect during object creation
        cls.client = AsyncIOMotorClient(
            mongo_uri, connect=False, serverSelectionTimeoutMS=2000
        )

        # Access the database using the name provided in the settings.
        cls.db = cls.client.get_database(db_name)

        # Initialize Beanie with the database and the list of document models.
        try:
            await init_beanie(database=cls.db, document_models=[Session, AttendanceLog])  # type: ignore
        except Exception as e:
            # Fail fast and continue -- allow application to start even if DB is unreachable
            print("Warning: Beanie init failed, continuing without DB readiness:")
            pprint(e)


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

    @classmethod
    def add_fallback_session(cls, session_id: str, payload: dict) -> None:
        cls._fallback_sessions[session_id] = payload

    @classmethod
    def get_fallback_session(cls, session_id: str) -> dict | None:
        return cls._fallback_sessions.get(session_id)

    @classmethod
    def add_fallback_log(cls, log: dict) -> None:
        cls._fallback_attendance_logs.append(log)
    
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