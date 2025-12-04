from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from .forms import PerfilUsuarioForm, UsuarioCrearForm, UsuarioEdicionForm
from .models import PerfilUsuario

User = get_user_model()


def _usuario_en_roles(usuario, roles):
    return usuario.is_superuser or usuario.groups.filter(name__in=roles).exists()


def requiere_roles(*roles):
    return user_passes_test(lambda u: u.is_authenticated and _usuario_en_roles(u, roles))


class PortalAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"form-control {existing_classes}".strip()


class LoginView(auth_views.LoginView):
    template_name = "cuentas/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("inicio")
    form_class = PortalAuthenticationForm


class LogoutView(auth_views.LogoutView):
    next_page = "login"


@login_required
def inicio(request):
    nombre_usuario = request.user.get_full_name() or request.user.username
    contexto = {
        "titulo": "Inicio",
        "saludo": f"Hola, {nombre_usuario}!",
    }
    return render(request, "inicio.html", contexto)


@login_required
def perfil(request):
    perfil_usuario, _ = PerfilUsuario.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = PerfilUsuarioForm(
            request.POST,
            request.FILES,
            instance=perfil_usuario,
            user=request.user,
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect("perfil")
    else:
        form = PerfilUsuarioForm(instance=perfil_usuario, user=request.user)

    contexto = {
        "titulo": "Mi Perfil",
        "form": form,
        "perfil": perfil_usuario,
    }
    return render(request, "cuentas/perfil.html", contexto)


@login_required
@requiere_roles("administrador", "gestor")
def usuarios_lista(request):
    usuarios = User.objects.all().order_by("username")
    es_admin = _usuario_en_roles(request.user, ["administrador"])
    contexto = {
        "titulo": "Usuarios",
        "usuarios": usuarios,
        "es_admin": es_admin,
    }
    return render(request, "cuentas/usuarios/lista.html", contexto)


@login_required
@requiere_roles("administrador")
def usuario_crear(request):
    if request.method == "POST":
        form = UsuarioCrearForm(request.POST)
        if form.is_valid():
            nuevo_usuario = form.save()
            messages.success(
                request, f"Usuario {nuevo_usuario.username} creado exitosamente."
            )
            return redirect("usuarios_lista")
    else:
        form = UsuarioCrearForm()

    contexto = {
        "titulo": "Crear usuario",
        "form": form,
        "accion": "Crear",
    }
    return render(request, "cuentas/usuarios/formulario.html", contexto)


@login_required
@requiere_roles("administrador", "gestor")
def usuario_editar(request, pk):
    usuario_objetivo = get_object_or_404(User, pk=pk)
    es_admin = _usuario_en_roles(request.user, ["administrador"])

    if not es_admin and (
        usuario_objetivo.is_superuser
        or _usuario_en_roles(usuario_objetivo, ["administrador"])
    ):
        messages.error(
            request, "No tienes permisos para editar un usuario administrador."
        )
        return redirect("usuarios_lista")

    if request.method == "POST":
        form = UsuarioEdicionForm(
            request.POST,
            instance=usuario_objetivo,
            include_rol=es_admin,
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado correctamente.")
            return redirect("usuarios_lista")
    else:
        form = UsuarioEdicionForm(instance=usuario_objetivo, include_rol=es_admin)

    contexto = {
        "titulo": f"Editar usuario {usuario_objetivo.username}",
        "form": form,
        "accion": "Guardar cambios",
        "usuario_objetivo": usuario_objetivo,
    }
    return render(request, "cuentas/usuarios/formulario.html", contexto)


@login_required
@requiere_roles("administrador")
def usuario_eliminar(request, pk):
    usuario_objetivo = get_object_or_404(User, pk=pk)

    if usuario_objetivo == request.user:
        messages.error(request, "No puedes eliminar tu propio usuario.")
        return redirect("usuarios_lista")

    if request.method == "POST":
        usuario_objetivo.delete()
        messages.success(request, "Usuario eliminado correctamente.")
        return redirect("usuarios_lista")

    contexto = {
        "titulo": f"Eliminar usuario {usuario_objetivo.username}",
        "usuario_objetivo": usuario_objetivo,
    }
    return render(request, "cuentas/usuarios/confirmar_eliminacion.html", contexto)
