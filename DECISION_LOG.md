# Decision Log

| # | Decision Point | Chosen Option | Why | Alternative Rejected |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Technology stack | Python, FastAPI, PostgreSQL | Fast development, strong built-in validation (Pydantic), auto-generated Swagger documentation, and simple containerization. | C# / .NET Core or Java / Spring Boot. (FastAPI delivers an MVP with less boilerplate in 3-4 hours). |
| 2 | Reservation cancellation approach | Soft delete (`POST /.../cancel` status change) | Keeping the database record is useful for auditing. The space is released again while preserving reservation history[cite: 3]. | Hard delete (physical removal using `DELETE`). |
| 3 | Overlap check logic | Service-layer validation via database query | While PostgreSQL `tsrange` could work, ORM/service-level validation is easier to test with in-memory SQLite[cite: 2]. | Pure database-level constraint (e.g. `EXCLUDE`). |
| 4 | Pydantic version | Pydantic V2 (`model_config = ConfigDict(...)`) | Latest FastAPI versions prefer Pydantic V2 for better performance and cleaner syntax[cite: 4, 5, 6]. | Pydantic V1 (`class Config`). |

## Short Reflection

The biggest challenge was handling reservation time overlap in a safe and efficient way. I initially considered purely database-level constraints, but moved the overlap check into the business logic (service layer) for better testability, enabling fast in-memory SQLite unit tests[cite: 2, 3]. In preparation for the optional feature, the database schema already stores parking space type information. I used AI assistance for validating the software architecture, designing Pydantic V2-specific configurations (such as `ConfigDict`)[cite: 4, 5, 6], and drafting Conventional Commit messages. The full prompt history is attached to the repository.