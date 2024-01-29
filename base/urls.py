
from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.home, name = "home"),
    path('login/', views.user_login, name='user_login'),
    path('signup/', views.signup, name='signup'),
    path('agency_admin_signup/',views.agency_admin_signup, name = "agency_admin_signup"),
    path('save_team_leader_details/<int:rescue_agency_id>/', views.save_team_leader_details, name='save_team_leader_details'),
    path('save_team_member_details/<int:rescue_agency_id>/', views.save_team_member_details, name='save_team_member_details'),
    #  path('agency_admin_dashboard/', views.agency_admin_dashboard, name='agency_admin_dashboard'),
    # path('team_leader_dashboard/', views.team_leader_dashboard, name='team_leader_dashboard'),
    # path('team_member_dashboard/', views.team_member_dashboard, name='team_member_dashboard'),
    path('dashboard/',login_required(views.dashboard), name = "dashboard"),
    path('profile/', views.view_rescue_agency_profile, name='rescue_agency_profile'),
    path('open_chat/', include('chat.urls')),
    path('view_resources/', include('resources.urls')),
    path('profile/', views.view_rescue_agency_profile, name='rescue_agency_profile'),
    path('my_agency_details/',views.my_agency_details, name = 'my_agency_details'),
]
