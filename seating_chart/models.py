from django.db import models

# Create your models here.
class SeatingChartModel(models.Model):
    num_section = models.IntegerField()
    desk_in_row = models.IntegerField()
    desk_in_column = models.IntegerField()
    shuffle = models.BooleanField(default=False)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)