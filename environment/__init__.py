import os 

from . import kubernetes
from . import kubernetes_production

ENVIRONMENT = os.environ['ORIHIME_DJANGO_ENVIRONMENT']

selected_module = locals()[ENVIRONMENT]
locals().update(selected_module.environment_settings)
__all__ = list(selected_module.environment_settings.keys())

