from rest_framework import serializers

from teams import models


class TeamSerializer(serializers.ModelSerializer):
    """
    Serializer for the Team model.
    """
    class Meta:
        fields = ('id', 'name')
        model = models.Team
