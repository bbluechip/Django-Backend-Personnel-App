from django.urls import path
from .views import *

urlpatterns = [
    path('department/', DeparmentView.as_view()),
    path('personnel/', PersonnelListCreateView.as_view()),
    path('personnel/<int:pk>', PersonalGetUpdateDelete.as_view()),
    path('department/<str:name>/', Custom.as_view()),
]
