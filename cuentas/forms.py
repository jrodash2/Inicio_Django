from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from .models import PerfilUsuario

User = get_user_model()


class PerfilUsuarioForm(forms.ModelForm):
    first_name = forms.CharField(label="Nombre", required=False)
    last_name = forms.CharField(label="Apellido", required=False)

    class Meta:
        model = PerfilUsuario
        fields = ["imagen", "first_name", "last_name"]
        widgets = {
            "imagen": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        self.user = user or kwargs.get("instance").user  # type: ignore[arg-type]
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields["first_name"].initial = self.user.first_name
            self.fields["last_name"].initial = self.user.last_name
        for name, field in self.fields.items():
            existing_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"form-control {existing_classes}".strip()
            field.widget.attrs.setdefault("placeholder", field.label)

    def save(self, commit=True):
        perfil = super().save(commit=False)
        self.user.first_name = self.cleaned_data.get("first_name", "")
        self.user.last_name = self.cleaned_data.get("last_name", "")
        if commit:
            self.user.save()
            perfil.user = self.user
            perfil.save()
        return perfil


class UsuarioCrearForm(UserCreationForm):
    rol = forms.ChoiceField(
        choices=[("administrador", "Administrador"), ("gestor", "Gestor")],
        label="Rol",
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "first_name", "last_name", "email", "rol"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            existing_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"form-control {existing_classes}".strip()
            field.widget.attrs.setdefault("placeholder", field.label)

    def save(self, commit=True):
        user = super().save(commit=False)
        rol = self.cleaned_data.get("rol")
        if commit:
            user.save()
            if rol:
                grupo, _ = Group.objects.get_or_create(name=rol)
                user.groups.set([grupo])
        return user


class UsuarioEdicionForm(forms.ModelForm):
    rol = forms.ChoiceField(
        choices=[("administrador", "Administrador"), ("gestor", "Gestor")],
        label="Rol",
        required=False,
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "is_active"]
        widgets = {
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "is_active": "Activo",
            "username": "Usuario",
            "first_name": "Nombre",
            "last_name": "Apellido",
            "email": "Correo",
        }

    def __init__(self, *args, include_rol=True, **kwargs):
        super().__init__(*args, **kwargs)
        if not include_rol:
            self.fields.pop("rol")
        else:
            current_group = (
                self.instance.groups.filter(name__in=["administrador", "gestor"]).first()
            )
            if current_group:
                self.fields["rol"].initial = current_group.name
        for name, field in self.fields.items():
            existing_classes = field.widget.attrs.get("class", "")
            if name == "is_active":
                continue
            field.widget.attrs["class"] = f"form-control {existing_classes}".strip()
            field.widget.attrs.setdefault("placeholder", field.label)

    def save(self, commit=True):
        user = super().save(commit=False)
        rol = self.cleaned_data.get("rol") if "rol" in self.cleaned_data else None
        if commit:
            user.save()
            if rol:
                grupo, _ = Group.objects.get_or_create(name=rol)
                user.groups.set([grupo])
        return user
