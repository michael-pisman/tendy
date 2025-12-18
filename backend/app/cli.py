import typer
import uvicorn

from app.config import Settings, set_settings, settings

# Create a Typer app instance for building command-line applications.
app = typer.Typer()


@app.command()
def start(
    # Server settings
    host: str = typer.Option(
        settings.host,
        "--host",
        "-h",
        help="The hostname to bind the server to.",
    ),
    port: int = typer.Option(
        settings.port,
        "--port",
        "-p",
        help="The port on which to run the server.",
    ),
    reload: bool = typer.Option(
        settings.reload,
        "--reload",
        "-r",
        help="Enable or disable automatic reloading of the server.",
    ),
    origins: str = typer.Option(
        "*",
        "--origins",
        "--cors",
        help="The origins of the API.",
    ),
    mongo_uri: str = typer.Option(
        settings.mongo_uri,
        "--mongo-uri",
        help="The URI for connecting to the MongoDB database.",
    ),
    mongo_dbname: str = typer.Option(
        settings.mongo_dbname,
        "--mongo-dbname",
        help="The name of the MongoDB database to use.",
    )

) -> None:
    """
    Start the FastAPI server using uvicorn.
    This command starts the uvicorn server by referencing the FastAPI application
    defined in the app module. It accepts parameters for host, port, reload, and a MongoDB URL.
    Args:
        host (str): The hostname to bind the server to. Defaults to "localhost".
        port (int): The port on which to run the server. Defaults to 8000.
        reload (bool): If True, enables auto-reload for development. Defaults to False.
        origins (str): The origins of the API. Defaults to "*".
    """

    set_settings(
        Settings(
            host=host,
            port=port,
            reload=reload,
            origins=origins,
            mongo_uri=mongo_uri,
            mongo_dbname=mongo_dbname,
        )
    )

    # Start the uvicorn server with the specified parameters.
    uvicorn.run(
        "app.app:app", reload=settings.reload, host=settings.host, port=settings.port
    )
