from django.db import models
from source.auth_service.models import User
from source.base.service import validate_size_image
from django.core import validators
from autoslug import AutoSlugField

class Club(models.Model):
    club_name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    club_logo = models.ImageField(
        upload_to='clubs/club_logos/',
        blank = True,
        null = True,
        validators = [validators.FileExtensionValidator(allowed_extensions=['png','jpeg','jpg']),validate_size_image]
    )
    members = models.ManyToManyField(User, through='ClubMembership',related_name='club_memberships')
    staff = models.ManyToManyField(User, through='ClubStaff',related_name='club_staff')
    slug = AutoSlugField(populate_from='club_name',unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self: str) -> str:
        return self.club_name
    
    def get_count_members(self):
        return self.members.count()
    
    def get_staff_count(self):
        return self.staff.count()


class ClubHead(models.Model):
    club_head = models.ForeignKey(User,on_delete=models.PROTECT)
    club = models.ForeignKey(Club,on_delete=models.CASCADE)
    def __str__(self:str) -> str:
        return f'{self.club}-{self.club_head}'
    

class ClubMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user} - {self.club} (Member)'


class ClubStaff(models.Model):
    STAFF_RANKS_CHOICES = [
        ('STAFF', 'Junior Staff'),
        ('PR', 'Mobilograph'),
        ('HR', 'HR Specialist'),
        ('VH', 'Vice Head'),
    ]

    rank_in_club = models.CharField(
        max_length=10,
        choices=STAFF_RANKS_CHOICES,
        default='STAFF'
    )
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    staff_user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.staff_user} - {self.club} ({self.rank_in_club})'


class ClubNews(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='news')
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self: str) -> str:
        return self.title    
        

class ClubPost(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='posts')
    poster = models.ForeignKey(ClubHead, on_delete=models.PROTECT,related_name='poster')
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=2000)
    image = models.ImageField(
        upload_to='clubs/club_posts/%Y/%m/%d/',
        blank=True,
        null=True,
        validators=[validators.FileExtensionValidator(allowed_extensions=['png','jpg','jpeg']),validate_size_image]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self: str) -> str:
        return f'{self.club} - {self.title}'    