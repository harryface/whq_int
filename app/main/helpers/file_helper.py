import csv, re, io
from django.db import connections
from rest_framework import exceptions

from main.models.time_sheet import TimeSheet
from main.tasks import create_report


class FileHelper:
    """helper methods for csv file"""

    @staticmethod
    def validate_csv(name):
        """checks if the csv file name has same ID as \
        one already processed in the system

        Args:
            uploaad (str): csv name

        Returns:
            file_id (str): csv file id
        """

        try:
            file_id = re.search('-([0-9]+).csv', name).group(1)
        except:
            file_id = None
        if not file_id:
            raise exceptions.ValidationError(
                'The CSV uploaded has wrong naming pattern')
        if TimeSheet.objects.filter(csv_file_id=file_id).exists():
            raise exceptions.ValidationError(
                'A CSV with this ID has already been uploaded')

        return file_id

    @staticmethod
    def update_timesheet_model(upload, csv_id):
        """utilizing postresql copy function, neglects \
        the header and populates the main_timesheet \
        table, with the csv data, trigger redis-celery \
        for later consumption
        
        Args:
            upload (file): csv

        Returns:
            None
        """

        io_string = io.StringIO(upload.read().decode())
        try:
            with connections['default'].cursor() as cursor:
                copy_sql = """
                    ALTER TABLE main_timesheet ALTER COLUMN \
                    csv_file_id SET DEFAULT {};
                    COPY main_timesheet (date, hours_worked, \
                    employee_id, job_group) FROM stdin WITH \
                    CSV HEADER DELIMITER as ','
                    """.format(csv_id)
                cursor.copy_expert(sql=copy_sql, file=io_string)

            create_report.delay(csv_id)
        except:
            raise exceptions.ParseError(
                                'Failed to parse the CSV file')

    @staticmethod
    def read_csv(upload):
        """reads the csv file and commit each line to \
        redis-celery for later consumption
        
        Args:
            upload (file): csv

        Returns:
            None
        """
        
        io_string = io.StringIO(upload.read().decode())
        
        try:
            data = csv.reader(io_string, delimiter=",")
            next(data, [])
            for row in data:
                create_report.delay(row)
        except csv.Error:
            raise exceptions.ParseError(
                'Failed to parse the CSV file')
