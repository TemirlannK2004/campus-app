from rest_framework import generics
from rest_framework import permissions 
from rest_framework.response import Response
from rest_framework.views import APIView
from source.club_service import models
from source.club_service.serializers import ClubSerializer,ClubPostSerializer,ClubNewsSerializer
from django.db.models import Q,Case,Count,F,Value,IntegerField,Prefetch
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework import status





# class ClubViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = models.ClubHead.objects.all()
#     serializer_class = ClubHeadSerializer

#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)


class ClubNewsAPI(generics.ListCreateAPIView):
    serializer_class = ClubNewsSerializer

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        club = get_object_or_404(models.Club, slug=slug)
        
        return models.ClubNews.objects.filter(club=club).order_by('-created_at')

    def perform_create(self, serializer):
        slug = self.kwargs.get('slug')
        club = get_object_or_404(models.Club, slug=slug)
        serializer.save(club=club)






class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
    
class ClubViewSet(viewsets.ReadOnlyModelViewSet ):
    permission_classes = [ReadOnly | permissions.IsAdminUser,]
    serializer_class = ClubSerializer
    lookup_field = 'slug'
    def get_queryset(self):
        slug = self.kwargs.get('slug')

        if not slug:
            return models.Club.objects.all().annotate(club_member_count = Count('members',distinct=True))
    
        return models.Club.objects.filter(slug=slug).annotate(
            club_member_count = Count('members',distinct=True),club_staff_count = Count('staff',distinct=True)
            ).prefetch_related(
                Prefetch('staff'    ,models.User.objects.only('first_name','last_name'))
            )


class ClubPostViewSet(viewsets.ModelViewSet):
    queryset = models.ClubPost.objects.all()
    serializer_class = ClubPostSerializer

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)

        post.save()
        serializer = ClubPostSerializer(post)
        return Response(serializer.data)