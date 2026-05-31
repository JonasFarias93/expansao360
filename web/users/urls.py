# web/users/urls.py
from django.urls import path
from users import views

app_name = "users"

urlpatterns = [
    path("", views.UsersHomeView.as_view(), name="home"),
    path("lista/", views.UserListView.as_view(), name="user_list"),
    path("novo/", views.UserCreateView.as_view(), name="user_create"),
    path("<int:user_id>/", views.UserDetailView.as_view(), name="user_detail"),
    path("<int:user_id>/editar/", views.UserEditView.as_view(), name="user_edit"),
    path("<int:user_id>/capabilities/", views.UserCapabilitiesView.as_view(), name="user_capabilities"),
]