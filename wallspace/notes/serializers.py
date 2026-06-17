from .models import Note

from rest_framework import serializers

class NoteSerializer(serializers.ModelSerializer):
    creator= serializers.ReadOnlyField(
        source='creator.username'
    )

    class Meta:
        model = Note
        fields=[
            'id',
            'title',
            'content',
            'color',
            'creator',
            'x_position',
            'y_position',
            'width',
            'height',
            'created_at',
            'updated_at'
        ]
