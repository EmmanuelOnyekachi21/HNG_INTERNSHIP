# Stage Zero Backend Task

This project is a simple Django REST API that returns user details, a random cat fact, and the current UTC timestamp.

## 🚀 How to Run Locally

### 1. Clone this repository
```
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

### 2. Create and activate a virtual environment
```
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
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
