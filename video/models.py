from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Video(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    video = models.FileField(upload_to='videos/')
    subtitles = models.FileField(upload_to='videos/')
    video_file_name = models.TextField()

    def __str__(self):
        return str(self.id)
