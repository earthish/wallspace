from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Wall(models.Model):
    title = models.CharField(max_length=100)
    owner=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='walls'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title #so it takes the title from the model while displaying a model
    
