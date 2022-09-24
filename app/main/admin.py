from django.contrib import admin
from main.models.report import Report
from main.models.time_sheet import TimeSheet


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """register report module for admin
    """

    list_display = (
        'employee_id', 'start_date',
        'end_date', 'amount_paid'
    )
    list_filter = ('employee_id', )


@admin.register(TimeSheet)
class TimeSheetAdmin(admin.ModelAdmin):
    """register timesheet module for admin
    """

    list_display = (
        'date', 'hours_worked',
        'employee_id', 'job_group',
        'csv_file_id'
    )
    list_filter = ('employee_id', )
