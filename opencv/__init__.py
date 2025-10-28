import pkgutil
import inspect
from django.db.models import Model

for (_, module_name, _) in pkgutil.iter_modules(__path__):
    module = __import__(f"{__name__}.{module_name}", fromlist=[module_name])
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and issubclass(obj, Model) and obj is not Model:
            globals()[name] = obj
