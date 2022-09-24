from django.db import models


class TimeSheet(models.Model):
    """
    Keep track of uploaded csv's data
    """
    date = models.CharField(max_length=10)
    hours_worked = models.FloatField()
    employee_id = models.IntegerField()
    job_group = models.CharField(max_length=1)
    csv_file_id = models.CharField(max_length=255)

    def __str__(self):
        return f"TimeSheet ID - {self.id}"
