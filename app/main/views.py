from rest_framework import generics, response, permissions, status
from rest_framework.parsers import MultiPartParser

from main.models.report import Report
from main.serializers import ReportSerializer, CsvFileSerializer


class CSVUploadView(generics.GenericAPIView):
    """Allows post verb with a csv for upload
    """
    
    serializer_class = CsvFileSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file_id = serializer.save()
        resp = {
            "message": f"CSV file with ID {file_id} uploaded successfully"
        }
        return response.Response(resp, status=status.HTTP_201_CREATED)


class ReportListView(generics.ListAPIView):
    """Allows get verb, for retrieving all report
    """

    queryset = Report.objects.all().order_by(
        "employee_id", "start_date")
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAdminUser]

    def list(self, _):
        queryset = self.get_queryset()
        serializer = ReportSerializer(queryset, many=True)
        return response.Response(
            serializer.data, status=status.HTTP_200_OK)
