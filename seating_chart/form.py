from django import forms
from .seating_chart import SeatingChart
from .models import SeatingChartModel
import os
import django
import csv

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "csgator.settings")
# django.setup()

# Query all records

# Print results
all_seating_charts = SeatingChartModel.objects.all()
# for seating_chart in all_seating_charts:
#    print(seating_chart)


class SeatingChartForm(forms.ModelForm):
    class Meta:
        model = SeatingChartModel
        fields = ['num_section', 'desk_in_row', 'desk_in_column', 'shuffle', 'file']

    def make_everything(self):
        try:
            seating_chart_info = SeatingChartModel.objects.latest('uploaded_at')
        except SeatingChartModel.DoesNotExist:
            raise ValueError("No seating chart records found!")
        # seating_chart_info = SeatingChartModel.objects.latest('uploaded_at')
        num_section = seating_chart_info.num_section
        desk_in_row = seating_chart_info.desk_in_row
        desk_in_column = seating_chart_info.desk_in_column
        shuffle = seating_chart_info.shuffle
        file_path = seating_chart_info.file.path
        new_student_name = []
        with open(file_path, 'r') as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                # print(f"📄 Reading row: {row}")
                first_name = row[0]
                last_name = row[1]
                new_student_name.append([first_name.title(), last_name.title()])
        student_names = new_student_name
        # print(f"👥 Processed student names: {student_names}")
        chart = SeatingChart(num_section, desk_in_row, desk_in_column, shuffle, student_names)
        chart.create_chart()
        chart.make_pdf()
        # return created_chart, pdfs







