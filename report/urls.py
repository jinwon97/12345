from . import views
from django.urls import path

app_name = 'report'

urlpatterns = [
    path("", views.inquire),
    path("recommendation/<business>/<seedMoney>", views.recommendation, name = "recommendation"),
]