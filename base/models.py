from django.db import models
from django.contrib.auth.models import User,Group
from django.core.validators import MinValueValidator

# Create your models here.
ORGANIZATION_TYPES = [
    ('tsunami', 'Tsunami'),
    ('flood', 'Flood'),
    ('cyclone', 'Cyclone'),
    ('earthquake', 'Earthquake'),
    ('storm', 'Storm'),
]


    
class Role(models.Model):
    USER_ROLES = [
        ('rescue_agency_admin', 'Rescue Agency Admin'),
        ('rescue_agency_team_leader', 'Team Leader'),
        ('rescue_agency_team_member', 'Team Member'),
    ]
    role = models.CharField(max_length=30, choices=USER_ROLES, default='rescue_agency_team_member')

    def __str__(self):
        return f'Role: {self.get_role_display()}'
    
    def get_group_name(self):
        return f'{self.role}_group' 
    

class RescueAgency(models.Model):
    organization_name = models.CharField(max_length=255)
    organization_type = models.CharField(max_length=20, choices=ORGANIZATION_TYPES)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    admin_name = models.CharField(max_length=255)
    team_member_count = models.IntegerField(default=1, null=True)
    team_leaders_count = models.IntegerField(default=1, null=True)
    organization_location = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    #profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.organization_name
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE,default=None, null=True)
    rescue_agency = models.ForeignKey(RescueAgency, on_delete=models.CASCADE, default=None, null=True)
    def __str__(self):
        return f'Profile for {self.user.username}'
    
class TeamMember(models.Model):
    member_name = models.CharField(max_length=255,default=None, null=True)
    rescue_agency = models.ForeignKey(RescueAgency, on_delete=models.CASCADE)
    is_team_leader = models.BooleanField(default=False)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, default=None, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return f'Team Member: {self.member_name}'

class TeamLeader(models.Model):
    
    leader_name = models.CharField(max_length=255,default=None, null=True) 
    rescue_agency = models.ForeignKey(RescueAgency, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, default=None, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return f'Team Leader: {self.leader_name}'
    
    
    
class TeamLeaderCount(models.Model):
    name = models.CharField(max_length=255)
    agency = models.ForeignKey(RescueAgency,on_delete=models.CASCADE)
    
class TeamMemberCount(models.Model):
    name = models.CharField(max_length=255)
    agency = models.ForeignKey(RescueAgency,on_delete=models.CASCADE)
    
    
