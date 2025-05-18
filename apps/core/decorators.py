# apps/core/decorators.py
# from django.contrib.auth.decorators import user_passes_test
# from django.conf import settings

# def group_required(group_name, login_url=None):
#     """
#     Solo permite acceso a usuarios autenticados en el grupo `group_name`.
#     Redirige al LOGIN_URL si no cumple.
#     """
#     login_url = login_url or settings.LOGIN_URL

#     def in_group(u):
#         return (
#             u.is_authenticated
#             and u.groups.filter(name=group_name).exists()
#         )

#     return user_passes_test(in_group, login_url=login_url)


# apps/core/decorators.py
from django.contrib.auth.decorators import user_passes_test

def group_required(group_name, login_url=None):
    """
    Sólo permite usuarios autenticados en `group_name`.
    Redirige a `login_url` si no cumple.
    """
    def in_group(u):
        return u.is_authenticated and u.groups.filter(name=group_name).exists()

    return user_passes_test(
        in_group,
        login_url=login_url  # puede ser 'mod1_login', 'mod2_login', …
    )
