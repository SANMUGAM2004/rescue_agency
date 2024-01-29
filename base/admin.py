from django.contrib import admin
from .models import RescueAgency
from .models import Profile
from .models import Role
from .models import TeamLeader
from .models import TeamMember,TeamLeaderCount,TeamMemberCount

admin.site.register(TeamMember)

admin.site.register(TeamLeader)

admin.site.register(RescueAgency)
admin.site.register(Profile)
admin.site.register(Role)
admin.site.register(TeamLeaderCount)
admin.site.register(TeamMemberCount)

