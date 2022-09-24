from django.urls import path
from main.views import CSVUploadView, ReportListView

urlpatterns = [
    path('reports/', ReportListView.as_view(), name='report'),
    path('payrolls/', CSVUploadView.as_view(), name="upload")
]