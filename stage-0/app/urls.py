from django.urls import path
from app.views import profile_view

urlpatterns = [
    path('me', profile_view, name='profile-view')
]