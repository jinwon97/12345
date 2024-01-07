from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("account.urls")),
    path('board/', include('board.urls')),
    # path('concernboard/', include('concernBoard.urls')),
    path('consultboard/', include('consultBoard.urls')),
    # path('reviewboard/', include('reviewBoard.urls')),
    path('announcements/', include('announcement.urls')),
    path('suggestions/', include('suggestions.urls')),
    path('faq/', include("faq.urls"))
]
