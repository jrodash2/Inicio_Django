from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("perfil/", views.perfil, name="perfil"),
    path("usuarios/", views.usuarios_lista, name="usuarios_lista"),
    path("usuarios/crear/", views.usuario_crear, name="usuarios_crear"),
    path("usuarios/<int:pk>/editar/", views.usuario_editar, name="usuarios_editar"),
    path("usuarios/<int:pk>/eliminar/", views.usuario_eliminar, name="usuarios_eliminar"),
    path("", views.inicio, name="inicio"),
]
