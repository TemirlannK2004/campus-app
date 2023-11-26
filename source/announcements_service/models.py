from django.db import models

# Create your models here.
class UniversityAnnouncement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
        
    
    def __str__(self):
        return self.title
        