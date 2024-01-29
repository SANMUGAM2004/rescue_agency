# forms.py
from django import forms
from .models import RescueAgency,Profile, TeamLeader,TeamMember,Role
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class RescueAgencySignupForm(forms.ModelForm):
    class Meta:
        model = RescueAgency
        fields = ['organization_name', 'organization_type', 'address', 'phone_number', 'admin_name', 'team_leaders_count','team_member_count', 'organization_location', 'latitude', 'longitude']

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        
class TeamLeaderDetailsForm(forms.ModelForm):
    class Meta:
        model = TeamLeader
        fields = ['leader_name', 'email', 'phone_number', 'common_password_team_leader']

    common_password_team_leader = forms.CharField(widget=forms.PasswordInput, required=False)
    leader_name = forms.CharField(required=False)

class TeamMemberDetailsForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['member_name', 'email', 'phone_number', 'common_password_team_member']

    common_password_team_member = forms.CharField(widget=forms.PasswordInput, required=False)
    member_name = forms.CharField(required=False)
    
    
class SimpleLoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)




# class CustomLoginForm(forms.Form):
#     username = forms.CharField(label='Username')
#     password = forms.CharField(widget=forms.PasswordInput, label='Password')
#     rescue_agency_name = forms.ChoiceField(choices=[], label='Rescue Agency')
#     role = forms.ChoiceField(choices=[], label='Role')

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         # Fetch choices from the database
#         rescue_agency_choices = [(agency.organization_name, agency.organization_name) for agency in RescueAgency.objects.all()]
#         role_choices = [(role.role, role.get_role_display()) for role in Role.objects.all()]

#         # Update choices for the fields
#         self.fields['rescue_agency_name'].choices = rescue_agency_choices
#         self.fields['role'].choices = role_choices
class CommonPasswordMixin(forms.Form):
    common_password = forms.CharField(widget=forms.PasswordInput, required=False)

class CustomLoginForm(AuthenticationForm, CommonPasswordMixin):
    rescue_agency_name = forms.ChoiceField(choices=[])
    role = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Fetch choices from the database
        rescue_agency_choices = [(agency.organization_name, agency.organization_name) for agency in RescueAgency.objects.all()]
        role_choices = [(role.role, role.get_role_display()) for role in Role.objects.all()]

        # Update choices for the fields
        self.fields['rescue_agency_name'].choices = rescue_agency_choices
        self.fields['role'].choices = role_choices