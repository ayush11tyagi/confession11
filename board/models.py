from django.db import models
from django.utils import timezone

# Create your models here.

class Confession(models.Model):
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Confession #{self.id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['-created_at']
