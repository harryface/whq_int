import unittest
from unittest.mock import patch

from main.tasks import create_report


class TestFileHelper(unittest.TestCase):
    """celery task test"""

    @patch('main.tasks.ReportHelper.update_or_create_report')
    def test_worker_success(self, u_or_c_report):
        """test if called, that it does what it should"""
        
        row = ["18/12/2023", "11.5", "3", "A"]
        create_report(row)
        u_or_c_report.assert_called_with(row)
