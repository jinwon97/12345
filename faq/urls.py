from django.urls import path
from . import views

urlpatterns = [
    path('faqlist/', views.FaqListView.as_view()),
    path('faqlist/<int:pk>', views.FaqView.as_view()),
    path('faqlist/createfaq', views.FaqCreateView.as_view()),
    path('faqlist/<int:pk>/updatefaq', views.FaqUpdateView.as_view()),
    path('faqlist/<int:pk>/deletefaq', views.FaqDeleteView.as_view()),
    path('faqlist/searchfaq/<str:searchfield>/<str:searchkeyword>', views.FaqSearchView.as_view()),
]