from django.urls import path
from . import views

urlpatterns = [
    
    path("dongestimate/<str:dong>/<str:business>/<int:funds>", views.dong_estimate.as_view()),
    path("dongpredict/<str:dong>/<str:business>/<int:funds>", views.dong_predict.as_view()),
    
    path("marketestimate/<str:market>/<str:business>/<int:funds>", views.market_estimate.as_view()),
    path("marketpredict/<str:market>/<str:business>/<int:funds>", views.market_predict.as_view()),
    
    
]