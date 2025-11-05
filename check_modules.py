import os
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'opencv.settings')
django.setup()

from airwrite.infrastructure.models.module import Module

modules = Module.objects.all()
print(f"Found {len(modules)} modules:")
for m in modules:
    print(f"- {m.name}: imagen={m.imagen}, url={m.imagen.url if m.imagen else 'None'}")