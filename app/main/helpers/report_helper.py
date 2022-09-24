import datetime

from main.models.report import Report
from main.models.time_sheet import TimeSheet


class ReportHelper:
    """helper methods for formating data for report"""

    @classmethod
    def over_time_implementation(cls, group):
        """group A overtime is 1.3, and group B is 1.25
            Args:

        """

        if group == "A":
            return 1.3
        else:
            return 1.25

    @classmethod
    def _convert_string_to_datetime(cls, date):
        """takes a str arg of format day/month/year and converts \
        it to a python date object, does on to calculate the \
        pay period 

        Args:
            date (str): dd/mm/yy

        Returns:
            tuple (date): [work date, start date, end date]
        """

        day, month, year = map(int, date.split("/"))

        start_date = datetime.date(year, month, 1)
        end_date = datetime.date(year, month, 15)
        if day > 15:
            start_date = datetime.date(year, month, 16)
            if month == 12:
                end_date = datetime.date(year, month, 31)
            else:
                end_date = datetime.date(year, month + 1, 1)\
                    - datetime.timedelta(days=1)

        return (start_date, end_date)

    @classmethod
    def group_wage_per_hour(cls, group):
        """computes the wage per job group

        Args:
            group (str): A or B ...

        Returns:
            wage (int): 20 or 30"""

        if group.upper() == "A":
            return (20, 1.3)
        elif group.upper() == "B":
            return (30, 1.25)
        else:
            return 0

    @classmethod
    def update_or_create_report(cls, csv_file_id):
        """
        - Filters TimeSheet with that csv_file_id, and
        - Check if a report for that employee at that time
        range exist, then compute the amount paid and add, else
        crete a totally new report with the appropriate information.

            Args:
                row (list): [date, hours worked, employee id,
                job group]

            Returns:
                None
        """

        time_sheet = TimeSheet.objects.filter(
                                csv_file_id=csv_file_id)

        for data in time_sheet:
            start_date, end_date = \
                cls._convert_string_to_datetime(data.date)
            wage_per_hour = cls.group_wage_per_hour(data.job_group)

            if Report.objects.filter(
                employee_id=data.employee_id,
                start_date=start_date,
                end_date=end_date
            ).exists():
                report = Report.objects.filter(
                    employee_id=data.employee_id,
                    start_date=start_date,
                    end_date=end_date
                ).first()

                report.amount_paid += wage_per_hour * float(data.hours_worked)
                report.save()

            else:
                Report.objects.create(
                    employee_id=data.employee_id,
                    start_date=start_date,
                    end_date=end_date,
                    amount_paid=wage_per_hour * float(data.hours_worked)
                )
