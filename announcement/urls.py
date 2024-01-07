from django.urls import path
from . import views

urlpatterns = [
    path('announcementlist/', views.AnnouncementListView.as_view()),
    path('announcementlist/<int:pk>', views.AnnouncementView.as_view()),
    path('announcementlist/createpost', views.AnnouncementCreateView.as_view()),
    path('announcementlist/searchpost/<str:searchfield>/<str:searchkeyword>', views.AnnouncementSearchView.as_view()),
    path('announcementlist/updatepost/<int:pk>', views.AnnouncementUpdateView.as_view()),
    path('announcementlist/deletepost/<int:pk>', views.AnnouncementdeleteView.as_view())
]