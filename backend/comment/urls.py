from django.urls import path
from .views import ListCreateComments

urlpatterns = [
    path('<int:post_id>/', ListCreateComments.as_view()),
]