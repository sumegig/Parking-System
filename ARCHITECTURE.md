# System Design and Architecture

## Architecture
The project follows a layered architecture based on the Separation of Concerns principle:
*   **API Layer (Routers):** Handles HTTP requests and performs Pydantic-based validation.
*   **Service Layer:** Implements business logic (for example, checking time overlaps during reservation creation).
*   **Data Access Layer (Repositories):** Isolates database operations.
*   **Data Model (Models):** SQLAlchemy ORM entities.

The system uses Pydantic V2 for data validation with `ConfigDict`[cite: 4, 5, 6]. For testing, it uses an in-memory SQLite database to enable fast and isolated execution[cite: 2].

## API Description

The REST API supports the following main operations:

### Parking Spaces
*   `GET /api/v1/parking-spaces`
    Returns a list of available parking spaces in the system[cite: 3].
*   `GET /api/v1/parking-spaces/{id}/reservations`
    Returns all reservations for a specific parking space.

### Reservations
*   `POST /api/v1/reservations`
    Creates a new reservation. The system validates that the start time is before the end time[cite: 6] and checks that no active reservation overlaps the requested interval[cite: 3].
*   `POST /api/v1/reservations/{id}/cancel`
    Cancels an existing reservation. The endpoint does not delete the record from the database, it updates the reservation status to `CANCELLED`, allowing the space to become available again[cite: 3].