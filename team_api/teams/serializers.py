from rest_framework import serializers

from teams import models


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Team model.
    """
    url = serializers.HyperlinkedIdentityField(view_name='teams:team-detail')

    class Meta:
        fields = ('url', 'name')
        model = models.Team
