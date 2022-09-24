import datetime
from unittest import TestCase, mock
from main.models.time_sheet import TimeSheet

from main.models.report import Report
from main.helpers.report_helper import ReportHelper


class TestReportHelper(TestCase):
    """tests for report helper
    """

    def setUp(self):
        """class wide variables
        """

        self.helpers = ReportHelper
        self.report = Report(
            id=1,
            employee_id="3",
            start_date=datetime.date(2023, 12, 16),
            end_date=datetime.date(2023, 12, 17),
            amount_paid=100.00)

        self.time_sheet = TimeSheet(
            id=1,
            employee_id=1,
            date="17/12/2022",
            hours_worked=5,
            job_group="A"
        )

    @mock.patch('main.helpers.report_helper.TimeSheet.objects')
    @mock.patch('main.helpers.report_helper.Report.objects')
    def test_update_report(self, report_mock, timesheet_mock):
        """test that a report was updated
        """

        timesheet_mock.filter.return_value = [self.time_sheet, ]
        report_mock.filter.return_value.exists.return_value = True
        first = report_mock.filter().first()
        first.return_value = mock.Mock(spec=self.report)

        self.helpers.update_or_create_report(1)
        first.save.assert_called()

    @mock.patch('main.helpers.report_helper.TimeSheet.objects.filter')
    @mock.patch('main.helpers.report_helper.Report.objects.create')
    @mock.patch('main.helpers.report_helper.Report')
    def test_create_report(self,
                report_mock, report_create_mock, timesheet_mock):
        """test that a new report was created
        """

        timesheet_mock.return_value = [self.time_sheet, ]
        report_mock.objects.filter.return_value.exists.return_value = False

        self.helpers.update_or_create_report(1)
        report_create_mock.assert_called_with(
            employee_id=self.time_sheet.employee_id,
            start_date=datetime.date(2022, 12, 16),
            end_date=datetime.date(2022, 12, 31),
            amount_paid=self.helpers._group_wage_per_hour(
            self.time_sheet.job_group) * float(self.time_sheet.hours_worked)
        )

    def test_convert_string_to_datetime(self):
        """
        Test that it converts the string appropriately
        """

        self.assertEqual(
            self.helpers._convert_string_to_datetime('16/11/2023'),
            (datetime.date(2023, 11, 16), datetime.date(2023, 11, 30))
        )
        self.assertEqual(
            self.helpers._convert_string_to_datetime('18/12/2023')[1],
            datetime.date(2023, 12, 31)
        )

    def test_group_wage_per_hour(self):
        """test if the method returns 20 for group A and 30 \
        for group B
        """

        self.assertEqual(
            self.helpers._group_wage_per_hour("A"),
            20
        )
        self.assertEqual(
            self.helpers._group_wage_per_hour("B"),
            30
        )
