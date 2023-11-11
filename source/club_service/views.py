from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from source.club_service import models
from source.club_service.serializers import AllClubsSerializer
# Create your views here.

class AllClubsView(ListAPIView):
    queryset = models.Club.objects.only('club_name','description','club_head__first_name')
    serializer_class = AllClubsSerializer
