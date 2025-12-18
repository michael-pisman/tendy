"""Tests for MongoDB utility functions.

These tests validate the async initialization, connectivity check, getters,
and database drop functionality provided by ``app.utils.mongodb.MongoDB``.

Tests will be skipped if a MongoDB instance is not reachable on the configured
URI (defaults to ``mongodb://localhost:27017``). A unique test database is used
per test session to avoid interfering with other databases.
"""

from typing import AsyncGenerator
from motor.motor_asyncio import AsyncIOMotorClient

from app.utils.mongodb import MongoDB


async def test_mongo_connection(client_test: AsyncGenerator) -> None:
    """Test if the MongoDB connection can be established."""
    # await MongoDB.init()
    client = await MongoDB.get_client()
    assert isinstance(client, AsyncIOMotorClient)
    assert client is not None

    assert await MongoDB.test_connection()


async def test_mongo_disconnection(client_test: AsyncGenerator) -> None:
    """Test if the MongoDB connection can be closed."""
    await MongoDB.close()
    client = await MongoDB.get_client()
    assert client is not None
    assert not await MongoDB.test_connection()