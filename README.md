# FastAPI CRUD Assignment

## Features

* FastAPI + SQLAlchemy
* SQLite (default) and PostgreSQL (via `DATABASE_URL` env var)
* CRUD endpoints for `Item` entity
* API Key authentication (`x-api-key` header)
* Pagination, filtering
* Custom SQL: average price
* Transaction example
* Tests with pytest + httpx
* Docker + docker-compose
* Alembic migrations (for schema management)

## Quick start (SQLite, local)

1. Create a virtualenv and install deps:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Run Alembic migrations (creates DB schema):

```bash
alembic upgrade head
```

3. Run the app:

```bash
uvicorn app.main:app --reload
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## PostgreSQL with Docker Compose

1. Ensure Docker and docker compose installed
2. Start services:

```bash
docker compose up --build
```

3. Apply migrations inside the container:

```bash
docker compose exec web alembic upgrade head
```

App will connect to Postgres via `DATABASE_URL` in compose file.

## API Key

The app expects header `x-api-key` for protected endpoints. Default in dev is `StantechAI` (or set `API_KEY` env var).

Example:

```http
x-api-key: StantechAI
```

## 📖 API Documentation & Endpoints

Once the app is running, you can explore the endpoints in **Swagger UI** and **ReDoc**:

* **Swagger UI** (interactive docs):
  👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

* **ReDoc** (alternative docs):
  👉 [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Available Endpoints

| Method   | Endpoint                    | Description                                             | Auth Required |
| -------- | --------------------------- | ------------------------------------------------------- | ------------- |
| `POST`   | `/items/`                   | Create a new item                                       | ✅ `x-api-key` |
| `GET`    | `/items/`                   | List items (supports `limit`, `offset`, `title` filter) | ❌             |
| `GET`    | `/items/{id}`               | Get a single item by ID                                 | ❌             |
| `PUT`    | `/items/{id}`               | Update an existing item                                 | ✅ `x-api-key` |
| `DELETE` | `/items/{id}`               | Delete an item                                          | ✅ `x-api-key` |
| `GET`    | `/items/meta/average_price` | Get average item price (custom SQL)                     | ❌             |
| `GET`    | `/health`                   | Health check                                            | ❌             |

## Tests

```bash
pytest -q
```

## Notes & Next steps

* This project is intentionally simple and suitable for the assignment. For production you'd add:

  * Use Alembic migrations (✅ already integrated)
  * Better error handling and validation
  * More complete authentication (JWT + refresh tokens)
  * CI configuration
