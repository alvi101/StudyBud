from django.urls import path
from . import views

# url file in the app
urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/<str:pk>/", views.profile, name="profile"),
    path("update/", views.update_user, name="update-user"),
    path("register/", views.register_view, name="register"),
    # does not work because needs id, url argument
    # path("room", room),
    # works
    path("room/<str:pk>/", views.room, name="room"),
    path("create-room/", views.create_room, name="create-room"),
    path("update-room/<str:pk>/", views.update_room, name="update-room"),
    path("delete-room/<str:pk>/", views.delete_room, name="delete-room"),
    path("delete-message/<str:pk>/", views.delete_message, name="delete-message"),
    path("topics/", views.topics, name="topics"),
]
