import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "opencv.settings")
django.setup()

from django.apps import apps
infra_models = apps.get_app_config('infrastructure').get_models()
print(list(infra_models))