# Parking-System

This project is a backend implementation of a parking reservation system built with Python and FastAPI.

## Running the Project

The system is designed to start with a single command and an initialized database. Docker and Docker Compose are required.

1. Clone the repository.
2. Open a terminal in the project root.
3. Run the following command:

    ```bash
    docker-compose up --build
    ```

This command starts the PostgreSQL database (initialized with reference data on startup) and the FastAPI backend service.

## Usage (API Documentation)

After the system starts successfully, the interactive API documentation (Swagger UI) is available at:
**http://localhost:8000/docs**

You can use this interface to test the endpoints through a web browser.