from rest_framework import serializers
from source.club_service import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['first_name','last_name']


class ClubHeadSerializer(serializers.ModelSerializer):
    club_head = UserSerializer()
    club = serializers.SerializerMethodField()
    class Meta:
        model=models.ClubHead
        fields = '__all__'

    def get_club(self,obj):
        return {"club_name": obj.club.club_name }   

class ClubStaffSerializer(serializers.ModelSerializer):
    staff_user = serializers.SerializerMethodField()
    class Meta:
        model=models.ClubStaff
        fields ="__all__"
    def get_staff_user(self,obj):
        return {
            "first_name": obj.staff_user.first_name ,
            "last_name": obj.staff_user.last_name 
            }   

class ClubSerializer(serializers.ModelSerializer):
    club_member_count = serializers.IntegerField(read_only=True)
    club_staff_count = serializers.IntegerField(read_only=True)
    staff = ClubStaffSerializer(source='clubstaff_set',many=True)
    head = ClubHeadSerializer(source='clubhead_set', many=True, read_only=True)
    class Meta:
        model = models.Club
        fields = ('club_name', 'description', 'club_logo', 'slug', 'is_active','club_member_count','club_staff_count','staff','head')
        lookup_field = 'slug'



class ClubPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClubPost
        fields = '__all__'
