from django.db import models

def uploadmodel_file_upload_to(instance, filename):
    return 'uploads/%s/%s' % (instance.user.username, filename)

class SegmentationPost(models.Model):
    author = models.CharField(max_length= 20)
    number_slide = models.IntegerField()
    original_file = models.FileField(upload_to=uploadmodel_file_upload_to)
    segm_file = models.FileField(upload_to=uploadmodel_file_upload_to)
    description = models.CharField(max_length= 20)