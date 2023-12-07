from django.urls import path

from . import views

app_name = 'AI-Alert'

urlpatterns = [
    path('list/inference/', views.inferenceList, name="inferenceList"),
    path('inference/<str:id>/', views.inferenceAlertList, name="inferenceAlertList")
]
