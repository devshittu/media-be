from rest_framework.response import Response
from rest_framework import status

class SoftDeleteMixin:
    """
    Mixin to override the default destroy method for soft delete.
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReportCreationMixin:
    def handle_post_report_creation(self, instance):
        instance.check_and_update_flag_status()
