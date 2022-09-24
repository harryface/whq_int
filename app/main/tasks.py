from celery import shared_task, exceptions, utils

from main.helpers.report_helper import ReportHelper

logger = utils.log.get_task_logger(__name__)

@shared_task
def create_report(csv_id):
    """call the update_or_create_report method of \
    ReportHelper
    """

    try:
        ReportHelper.update_or_create_report(csv_id)
    except exceptions.OperationalError:
        pass
