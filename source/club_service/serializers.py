from rest_framework import serializers
from source.club_service import models


class AllClubsSerializer(serializers.ModelSerializer):
    club_head_full_name = serializers.SerializerMethodField()
    class Meta:
        model = models.Club
        fields = ['id','club_name','description','club_head_full_name']

    def get_club_head_full_name(self, obj):
        if obj.club_head:
            return f'{obj.club_head.first_name} {obj.club_head.last_name}' 
        return None
