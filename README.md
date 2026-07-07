# DocuMind

Minimal FastAPI foundation for the DocuMind MVP.

## Local setup

1. Start the app and database:

   ```sh
   docker compose up --build
   ```

   Older Docker installs may need `docker-compose up --build`.

2. Check the API:

   ```sh
   curl http://localhost:8000/health
   ```

Expected response:

```json
{"status":"ok","database":"ok"}
```

## Development

Create `.env` from `.env.example` only when you need to override local defaults.

Install dependencies locally if you want to run tests outside Docker:

```sh
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
pytest
```
