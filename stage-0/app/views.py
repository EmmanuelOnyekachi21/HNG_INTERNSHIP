from rest_framework.decorators import api_view
import requests
from rest_framework.response import Response
from datetime import datetime
from rest_framework import status
from decouple import config

@api_view(['GET'])
def profile_view(request):
    # Creating static user data
    user = {
        "email": config("EMAIL"),
        "name": config("NAME"),
        "stack": config("STACK"),
    }

    # Getting radom fact from catfact API
    try:
        # Use requests to get data from api
        response = requests.get(config('CATFACT_URL'), timeout=3)
        data = response.json()
        fact = data['fact']
    except Exception as e:
        fact = "Can't fetch fact at the time."
    
    # Generate current UTC 
    timestamp = datetime.utcnow().isoformat() + 'Z'

    response_data = {
            "status": "success",
            "user": user,
            "timestamp": timestamp,
            "fact": fact
        }
    return Response(response_data, status=status.HTTP_200_OK)

    

