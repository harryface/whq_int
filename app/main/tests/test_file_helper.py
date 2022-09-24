from unittest import TestCase, mock

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import DEFAULT_DB_ALIAS

from rest_framework import exceptions

from main.models.time_sheet import TimeSheet
from main.helpers.file_helper import FileHelper


class TestFileHelper(TestCase):
    """tests for the file helper"""

    def setUp(self):
        """class wide variables"""

        self.helpers = FileHelper
        self.report = TimeSheet(
            id=1,
            employee_id=1,
            date="17/12/2022",
            hours_worked=5,
            job_group="A"
        )

    @mock.patch('main.helpers.file_helper.TimeSheet')
    def test_validate_csv_raises_exception(self, ts_mock):
        """test that exceptions are thrown when csv is of \
        wrong format as well as when the id exists.
        """

        ts_mock.objects.filter().exists().return_value = True
        ts_mock.objects.filter().return_value = self.report

        with self.assertRaises(exceptions.ValidationError):
            self.helpers.validate_csv("testing-testing.csv")

        with self.assertRaises(exceptions.ValidationError):
            self.helpers.validate_csv("testing-testing-2.csv")

    @mock.patch('main.helpers.file_helper.TimeSheet.objects')
    def test_validate_csv(self, ts_mock):
        """test that a csv with appropriate naming and \
        not in database returns the file id
        """

        ts_mock.filter.return_value.exists.return_value = False

        id = self.helpers.validate_csv("testing-testing-2.csv")
        self.assertEqual(id, '2')

    @mock.patch('main.helpers.file_helper.io.StringIO')
    @mock.patch('main.helpers.file_helper.create_report.delay')
    @mock.patch('main.helpers.file_helper.csv.reader')
    def test_read_csv(self, csv_mock, create_report_mock, _):
        """test that a new report was created
        """

        uploaded_file = mock.Mock(spec=InMemoryUploadedFile)

        csv_mock.return_value = iter(([], ["4/1/2023", 10, 1, "A"]))

        self.helpers.read_csv(uploaded_file)
        create_report_mock.assert_called_with(["4/1/2023", 10, 1, "A"])

    @mock.patch('main.helpers.file_helper.io.StringIO')
    @mock.patch('main.helpers.file_helper.create_report.delay')
    @mock.patch('main.helpers.file_helper.connections')
    def test_some_function_executes_some_sql(self,
            mock_connections, create_report_mock, io_string_mock):
        """test that timesheet was populated and report creation \
            started
        """

        csv_file_id = 2
        mock_cursor = mock_connections.__getitem__(DEFAULT_DB_ALIAS)\
            .cursor.return_value.__enter__.return_value

        uploaded_file = mock.Mock(spec=InMemoryUploadedFile)
        self.helpers.update_timesheet_model(uploaded_file, csv_file_id)

        mock_cursor.copy_expert.assert_called_once()
        create_report_mock.assert_called_with(csv_file_id)
