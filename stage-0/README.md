# Stage Zero Backend Task

This project is a simple Django REST API that returns user details, a random cat fact, and the current UTC timestamp.

## 🚀 How to Run Locally

### 1. Clone this repository
```
git clone git@github.com:EmmanuelOnyekachi21/HNG_INTERNSHIP.git
cd HNG_INTERNSHIP
```

### 2. Create and activate a virtual environment
```
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Create a .env file in the project root
```
EMAIL=your_email@example.com
NAME=<your>
STACK=<your stack>
CATFACT_URL=https://catfact.ninja/fact
```


### 5. Run the server
```
python manage.py runserver
```

### 6. Test Endpoint
```
Open http://127.0.0.1:8000/me
```

### 7. 🌐 Endpoint
```
{
  "status": "success",
  "user": {
    "email": "nnabugwueo@gmail.com",
    "name": "Emmanuel Onyekachi",
    "stack": "backend"
  },
  "timestamp": "2025-10-19T12:00:00Z",
  "fact": "Cats have five toes on their front paws, but only four on the back."
}
```
