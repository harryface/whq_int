from rest_framework import serializers, exceptions

from main.models.report import Report

from main.helpers.file_helper import FileHelper


class CsvFileSerializer(serializers.Serializer):
    """Serializer for the receiving the uploded csv
    """
    
    csv_file = serializers.FileField(write_only=True)

    def save(self):
        """ receives a CSV uploaded file, validates it,
        then go ahead to save it on timesheet database,
        then return the id.
        """

        csv_file = self.validated_data.get("csv_file", None)
        if not csv_file:
            raise exceptions.ValidationError(
                                    "File not uploaded")
        file_id = FileHelper.validate_csv(csv_file.name)
        FileHelper.update_timesheet_model(csv_file, file_id)

        return file_id


class ReportSerializer(serializers.ModelSerializer):
    """Serializer for the Report model
    """

    class Meta:
        model = Report
        fields = ['employee_id', 'start_date', 'end_date',
                  'amount_paid']

    def to_representation(self, instance):
        """Method to be used to put the response in \
        the desired format
        """

        data = super().to_representation(instance)

        # start_date = data.pop('start_date')
        data["pay_period"] = {
            "start_date": data.pop('start_date'),
            "end_date": data.pop('end_date')
        }
        data["amount_paid"] = "${:.2f}".format(
            data.pop('amount_paid'))

        response = {
                    "payroll_report": {
                        "employee_reports": data
                    }
                }
        return response
