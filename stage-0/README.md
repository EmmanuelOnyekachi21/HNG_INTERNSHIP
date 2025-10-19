### This is stage 0 of the Backend Track

# Backend Wizards Stage 0 — Dynamic Profile Endpoint

## Setup Instructions
1. Clone this repository
2. Create a virtual environment
3. Install dependencies from `requirements.txt`
4. Create a `.env` file if needed
5. Run the server: `python manage.py runserver`

## Endpoint
GET /me

Response Example:
```
{
  "status": "success",
  "user": {
    "email": "example@mail.com",
    "name": "John Doe",
    "stack": "Python/Django"
  },
  "timestamp": "2025-10-19T09:22:33.900Z",
  "fact": "Cats sleep 70% of their lives."
}
```

## External API
Cat Facts API: https://catfact.ninja/fact

