import os
import sys
from django.conf import settings
from django.core.management import execute_from_command_line

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY="segredo-para-testes-e-desenvolvimento",
        ROOT_URLCONF="manage",
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
            }
        },
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "django.contrib.auth",
            "plantas",
        ],
        MIDDLEWARE=[
            "django.middleware.common.CommonMiddleware",
        ],
    )

from django.urls import path
from plantas import listar_plantas, criar_planta

urlpatterns = [
    path("", listar_plantas),
    path("criar/", criar_planta),
]

if __name__ == "__main__":
    execute_from_command_line(sys.argv)