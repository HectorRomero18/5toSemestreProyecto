from django.apps import AppConfig

class InfrastructureConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'airwrite.infrastructure'

    def ready(self):
        import airwrite.infrastructure.signals

