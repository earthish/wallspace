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
    
class WallMember(models.Model):
    ROLE_CHOICES=[
        ("viewer","Viewer"),
        ("editor","Editor"),
    ]

    wall=models.ForeignKey(
        Wall,
        on_delete=models.CASCADE,
        related_name="members"
    )

    user=models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="viewer"
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="viewer"
    )

    class Meta:
        unique_together=("wall","user")

    def __str__(self):
        return f"{self.user.username} - {self.role}"