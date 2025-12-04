from django.core.management.base import BaseCommand

from ._bootstrap_portal import bootstrap_portal_data


class Command(BaseCommand):
    help = (
        "Configura grupos de permisos y crea usuarios iniciales para el portal. "
        "Ejecutar después de 'migrate'."
    )

    def handle(self, *args, **options):
        bootstrap_portal_data(stdout=self.stdout, style=self.style)
