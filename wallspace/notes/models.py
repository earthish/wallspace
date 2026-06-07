from django.db import models
from django.contrib.auth.models import User
from walls.models import Wall

# Create your models here.

class Note(models.Model):
    
    COLOR_CHOICES = [#COLOR_CHOICES is a list of tuples
        # formatted like this: (database_value, human_readable_label)
        ('yellow','Yellow'),
        ('pink', 'Pink'),
        ('blue', 'Blue'),
        ('green', 'Green'),
    ]

    wall = models.ForeignKey( #foreign key
        Wall,
        on_delete=models.CASCADE,
        related_name='notes'
    )

    creator=models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=100,
        blank=True
    )

    content = models.TextField()

    color= models.CharField(
        max_length=20,
        choices=COLOR_CHOICES,
        default='yellow'
    )
    x_position = models.IntegerField(
        default=50
    )

    y_position = models.IntegerField(
        default=50
    )
    width = models.IntegerField(
    default=220
    )

    height = models.IntegerField(
    default=120
    )



    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):
        return f'{self.creator} note'

