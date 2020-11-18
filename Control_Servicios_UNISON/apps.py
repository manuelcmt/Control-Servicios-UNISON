from django.apps import AppConfig


class ControlServiciosUnisonConfig(AppConfig):
    name = 'Control_Servicios_UNISON'


    def ready(self):
        import Control_Servicios_UNISON.signals