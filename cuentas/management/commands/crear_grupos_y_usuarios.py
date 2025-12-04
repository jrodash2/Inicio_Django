from django.core.management.base import BaseCommand

from ._bootstrap_portal import bootstrap_portal_data


class Command(BaseCommand):
    help = (
        "Crea los grupos 'administrador' y 'gestor' y genera los usuarios "
        "iniciales jrodas y rodas con sus permisos. Ejecutar después de las "
        "migraciones."
    )

    def handle(self, *args, **options):
        bootstrap_portal_data(stdout=self.stdout, style=self.style)
