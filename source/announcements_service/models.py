from django.db import models
from source.base.service import validate_size_image
from django.core import validators
# Create your models here.
class UniversityAnnouncement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
    
class AnnouncementImage(models.Model):
    announcement = models.ForeignKey(UniversityAnnouncement,on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='announcements/',
        blank=True,
        null=True,
        validators=[validators.FileExtensionValidator(allowed_extensions=['png','jpg','jpeg']),validate_size_image]
        )
    
    
    def __str__(self) -> str:
        return f'{self.announcement.title}'