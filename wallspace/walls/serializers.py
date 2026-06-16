from rest_framework import serializers
from .models import Wall

class WallSerializer(serializers.ModelSerializer):
    owner=serializers.ReadOnlyField(
        source='owner.username'
    )

    class Meta:
        model = Wall
        fields=[
            'id',
            'title',
            'owner',
            'created_at'
        ]