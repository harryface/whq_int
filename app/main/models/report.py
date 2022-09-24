from django.db import models

from main.helpers.report_helper import ReportHelper


class Report(models.Model):
    """keep track of report model.
    - used TextField instead of CharField because
      I dont have an idea of its char lenght
    - assumed that an employee can work both groups,
      because of that did not take record of hours
      worked or have a calculated field for amount
      paid, rather amount paid."""

    employee_id = models.TextField(null=False)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    hours_worked = models.FloatField(null=True)
    job_group = models.CharField(max_length="A")

    @property
    def amount_paid(self):
        """For any job above 40 hrs, multiply the excesses
        by 1.25"""
        wage, overtime = ReportHelper.group_wage_per_hour(self.job_group)
        if self.hours_worked > 40:
            extra_hours = self.hours_worked - 40
            return (40 * wage) + (extra_hours * wage * overtime)
        else:
            return self.hours_worked * wage

    def __str__(self):
        return f"Report - {self.id}"
