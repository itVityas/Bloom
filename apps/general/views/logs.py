import os

from django.http import FileResponse, Http404, HttpResponse
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from Bloom import settings
from apps.general.permission import LogsPermission
from apps.general.serializers.logs import LogDownloadSerializer


class BaseLogDownloadView(GenericAPIView):

    serializer_class = LogDownloadSerializer
    permission_classes = [IsAuthenticated, LogsPermission]

    log_filename = None

    def get(self, request):
        if not self.log_filename:
            raise Http404("Log filename not specified")

        log_path = os.path.join(settings.BASE_DIR, 'logs', self.log_filename)
        if not os.path.exists(log_path):
            raise Http404(f"Log file not found: {self.log_filename}")

        try:
            with open(log_path, 'rb') as f:
                data = f.read()
        except Exception as e:
            raise Http404(f"Cannot read log file: {e}")

        response = HttpResponse(data, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{self.log_filename}"'
        return response

@extend_schema(tags=['Logs'])
@extend_schema_view(
    get=extend_schema(
        summary='Get django log file as attachment.',
        description='Permission: Admin',
    )
)
class LogDjangoDownloadView(BaseLogDownloadView):
    """
    GET /api/v1/logs/django_download/
    """
    log_filename = 'django.log'


@extend_schema(tags=['Logs'])
@extend_schema_view(
    get=extend_schema(
        summary='Get omega log file as attachment.',
        description='Permission: Admin',
    )
)
class LogOmegaDownloadView(BaseLogDownloadView):
    """
    GET /api/v1/logs/omega_download/
    """
    log_filename = 'omega.log'
