from rest_framework import serializers
from .models import Wall, WallMember


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

from .models import WallMember


class WallMemberSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = WallMember
        fields = [
            'id',
            'user',
            'role'
        ]

class InviteMemberSerializer(serializers.Serializer):

    username = serializers.CharField(
        max_length=150
    )

    role = serializers.ChoiceField(
        choices=[
            ('viewer', 'Viewer'),
            ('editor', 'Editor')
        ]
    )