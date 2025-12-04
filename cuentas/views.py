from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy


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
