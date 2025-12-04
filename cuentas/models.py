from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


def perfil_upload_to(instance, filename):
    return f"perfiles/{instance.user.username}/{filename}"


class PerfilUsuario(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to=perfil_upload_to, blank=True, null=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(user=instance)
