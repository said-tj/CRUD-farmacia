# apps/core/apps.py

from django.apps import AppConfig

class CoreConfig(AppConfig):
    name = 'apps.core'

    def ready(self):
        # Importamos aquí para no hacerlo antes de tiempo
        from django.db.utils import OperationalError
        from django.contrib.auth.models import Group

        # Intentamos crear los grupos, pero si la tabla auth_group
        # aún no existe (antes de migrate), simplemente lo ignoramos.
        try:
            for i in range(1, 8):
                Group.objects.get_or_create(name=f'Módulo{i}')
        except OperationalError:
            pass
