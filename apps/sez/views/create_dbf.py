import os
import tempfile

from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView

from apps.sez.serializers.create_dbf import DBFZipSerializer
from apps.sez.clearance_workflow.create_dbf.generate_all_dbf import generate_all_dbf_zip

class ClearanceInvoiceDBFZipView(GenericAPIView):
    """
    GET /api/clearance-invoices/{clearance_invoice_id}/dbf-zip/
    """
    serializer_class = DBFZipSerializer

    def get(self, request, clearance_invoice_id):
        # 1. Валидация
        serializer = self.get_serializer(
            data={'clearance_invoice_id': clearance_invoice_id}
        )
        serializer.is_valid(raise_exception=True)

        # 2. Создаем временный файл
        tmp_file = tempfile.NamedTemporaryFile(
            suffix='.zip', delete=False
        )
        tmp_file.close()  # закроем, чтобы generate_all_dbf_zip мог перезаписать
        tmp_path = tmp_file.name

        try:
            # 3. Генерируем ZIP
            generate_all_dbf_zip(clearance_invoice_id, tmp_path)

            # 4. Читаем содержимое и сразу удаляем файл
            with open(tmp_path, 'rb') as f:
                data = f.read()
            os.remove(tmp_path)

            # 5. Отдаем ZIP как attachment
            resp = HttpResponse(
                data,
                content_type='application/zip'
            )
            resp['Content-Disposition'] = (
                f'attachment; filename="invoice_{clearance_invoice_id}_dbf.zip"'
            )
            return resp

        except Exception as e:
            # убираем tmp даже при ошибке
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            return HttpResponse(
                f"Error generating DBF ZIP: {e}",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
