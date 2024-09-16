from django.contrib import admin
from django.urls import path, include

# request is the http request that comes
# from the user
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("base.urls")),
    path("api/", include("base.api.urls")), 
]
