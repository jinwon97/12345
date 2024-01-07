from django.urls import path
from . import views

urlpatterns = [
    path('suggestions/', views.SuggestionListView.as_view()),
    path('suggestions/<int:pk>', views.SuggestionView.as_view()),
    path('suggestions/createpost', views.SuggestionCreateView.as_view()),
    path('suggestions/searchpost/<str:searchfield>/<str:searchkeyword>', views.SuggestionSearchView.as_view()),
    path('suggestions/updatepost/<int:pk>', views.SuggestionUpdateView.as_view()),
    path('suggestions/deletepost/<int:pk>', views.SuggestionDeleteView.as_view())
]