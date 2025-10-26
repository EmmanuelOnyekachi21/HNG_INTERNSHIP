# Stringify — String Analysis API

Small Django + DRF API that analyzes strings and stores computed properties (length, palindrome, char frequencies, etc.).
This repo provides endpoints to create/analyze strings, query/filter them, parse simple natural-language filters, and delete entries.

## Quick Status
- Framework: Django 4.x + Django REST Framework
- DB (local dev): SQLite (default). Production: PostgreSQL recommended.
- App: core
- Endpoints base: /api/

## Table of Contents
1. Setup (local)
2. Environment variables
3. Run locally
4. Migrations
5. API endpoints & examples
6. Testing
7. Repo checklist (what to include)

### 1- Setup
#### Recommended: Use a virtual environment
```bash
# clone
git clone <your-repo-url>
cd stringify

# create venv
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate    # Windows PowerShell

# install
pip install -r requirements.txt
```

### 2 — Environment variables

Create a .env file (or export env vars) for local dev if you use django-environ or similar. Minimal set:
```bash
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 3 — Run locally
```bash
# run migrations
python manage.py migrate

# create a superuser (optional)
python manage.py createsuperuser

# run server
python manage.py runserver
```
##### Open: [localhost](http://127.0.0.1:8000/)
##### API base (example): http://127.0.0.1:8000/api/

### 4 — Migrations & DB

- Create migrations: ```python manage.py makemigrations```
- Apply: python manage.py migrate
- If you switch to Postgres locally, update ```DATABASE_URL``` and install ```psycopg2-binary```.

### 5 — API Endpoints & Example Requests

Base prefix used in README: ```/api/```

1) #### Create/Analyze and Save

    POST ```/api/create_string/```
    
    Request body (JSON)
    ```json
    { "value": "string to analyze" }
    ```
    Success 201:
    ```json
    {
        "id": "sha256_hash_value",
        "value": "string to analyze",
        "properties": {
            "length": 16,
            "is_palindrome": false,
            "unique_characters": 12,
            "word_count": 3,
            "sha256_hash": "abc123...",
            "character_frequency_map": { "s": 2, "t": 3, "r": 2 }
        },
        "created_at": "2025-08-27T10:00:00Z"
    }
    ```
    Errors:
    - 400 — Invalid or missing value field: {"value": "Invalid request body or missing \"value\" field"}
    - 422 — Invalid data type for value: {"value": "Invalid data type for \"value\" (must be string)"}
    - 409 — Duplicate string: {"value": "String already exists in the system"}

    Example ```curl```:
    ```bash
    curl -X POST http://127.0.0.1:8000/api/create_string/ \
    -H "Content-Type: application/json" \
    -d '{"value":"radar"}'
    ```

2) #### Get specific string

    GET ```/api/strings/<string_value>/```

    Example:
    GET ```/api/strings/radar/```

    Success (200): same schema as POST response.
    404 if not found:

    ```json
    {"detail":"String does not exist in the system"}```

3) #### List & Filtering

    GET ```/api/strings/```

    Query params supported:

    - ```is_palindrome``` (true/false)
    - ```min_length``` (int)
    - ```max_length``` (int)
    - ```word_count``` (int)
    - ```contains_character``` (single char)

    Example:
    GET ```/api/strings/?is_palindrome=true&min_length=5&contains_character=a```

    Response:
    ```json
    {
        "data": [ /* items as above */ ],
        "count": 15,
        "filters_applied": {
            "is_palindrome": true,
            "min_length": 5,
            "contains_character": "a"
        }
    }
    ```

4) #### Natural Language Filtering

    GET ```/api/strings/filter-by-natural-language/?query=<your query>```

    Examples supported:
    - ```single word palindromic strings ```→ ```{"is_palindrome": true, "word_count":1}```
    - ```strings longer than 10 characters``` → ```{"length__gt":10}```
    - ```palindromic strings that contain the letter a``` → ```{"is_palindrome":true, "value__icontains":"a"}```

    ##### Response:
    ```json
    {
        "data": [ /* matching items */ ],
        "count": 3,
        "interpreted_query": {
            "original": "all single word palindromic strings",
            "parsed_filters": { /* filters used */ }
        }
    }
    ```
    ##### Errors:
    - 400 — missing query or cannot parse
    - 422 — parsed but conflicting filters

5) #### Delete string

    DELETE ```/api/strings/<string_value>/```

    Success: 204 No Content (empty body)
    404 if not found:
    ```json
    {"error":"String not found"}
    ```

