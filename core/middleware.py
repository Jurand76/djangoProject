from django.utils.deprecation import MiddlewareMixin
from core.models import Tenant
import logging


logger = logging.getLogger(__name__)

class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # get domain from header of HTTP_HOST
        domain = request.META.get('HTTP_HOST', '').split(':')[0]  # Ignorujemy port
        try:
            request.tenant = Tenant.objects.get(domain=domain)
            logger.info(f"Tenant found: {request.tenant}")
        except Tenant.DoesNotExist:
            request.tenant = None
            logger.warning("No tenant found for domain: %s", domain)