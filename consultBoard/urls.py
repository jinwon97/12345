from django.urls import path
from . import views

urlpatterns = [
    path('postlist/', views.BoardPostListView.as_view()),
    path('postlist/<int:pk>', views.BoardPostView.as_view()),
    path('postlist/createpost', views.BoardPostCreateView.as_view()),
    path('postlist/<int:pk>/updatepost', views.BoardPostUpdateView.as_view()),
    path('postlist/<int:pk>/deletepost', views.BoardPostDeleteView.as_view()),
    path('postlist/searchpost/<str:searchfield>/<str:searchkeyword>', views.BoardSearchView.as_view()),
    
    path('postlist/<int:pk>/comment', views.BoardPostCommentView.as_view()),
    path('postlist/<int:pk>/createcomment', views.BoardPostCommentCreateView.as_view()),
    path('postlist/updatecomment/<int:pk>', views.BoardPostCommentUpdateView.as_view()),
    path('postlist/deletecomment/<int:pk>', views.BoardPostCommentDeleteView.as_view()),
]