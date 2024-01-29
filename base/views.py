from django.shortcuts import render,redirect,get_object_or_404
from .forms import RescueAgencySignupForm, SignUpForm ,TeamLeaderDetailsForm,TeamMemberDetailsForm,CustomLoginForm,SimpleLoginForm
from .models import Profile,TeamMemberCount,TeamLeaderCount,Role, RescueAgency,TeamLeader,TeamMember
from  django.views import View
from django.contrib.auth import login,authenticate,get_user_model
from django.contrib.auth.models import Group,User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from resources.models import Resource



def home(request):
    return render(request, 'base/home.html')

def agencyadminlogin(request):
    return render(request,'base/agency_admin_login')

def agency_admin_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            role, created = Role.objects.get_or_create(role='rescue_agency_admin')
            user.role = role
            group, created = Group.objects.get_or_create(name=role.get_group_name())
            user.groups.add(group)
            user.save()
            profile = Profile.objects.create(user=user)
            profile.role = role
            profile.save()
            login(request, user)
            return redirect('signup')
    else:
        form = SignUpForm()

    return render(request, 'base/agency_admin_signup.html', {'form': form})
    

def signup(request):
    if request.method == 'POST':
        form = RescueAgencySignupForm(request.POST)
        if form.is_valid():
            rescue_agency = form.save(commit=False)
            role, created = Role.objects.get_or_create(role='rescue_agency_admin') 
            rescue_agency.role = role
            rescue_agency.profile = request.user.profile  
            rescue_agency.save()
            id=rescue_agency.id
            agent=RescueAgency.objects.get(id=id)
            profile = get_object_or_404(Profile, user=request.user)
            profile.rescue_agency = rescue_agency
            team_leaders_count = rescue_agency.team_leaders_count
            for x in range(team_leaders_count):
                leader=TeamLeaderCount.objects.create(name="name",agency=agent)
            team_leader_forms = TeamLeaderDetailsForm()
            team_leaders_count = int(team_leaders_count)
            count=TeamLeaderCount.objects.all()
            return render(request, 'base/team_leader_details.html', {'rescue_agency': rescue_agency, 'team_leader_forms': team_leader_forms,'team_leaders_count':count})

    else:
        form = RescueAgencySignupForm()

    return render(request, 'base/signup.html', {'form': form})

def save_team_leader_details(request, rescue_agency_id):
    rescue_agency = RescueAgency.objects.get(id=rescue_agency_id)
    print(request.POST)
    if request.method == 'POST':
        common_password_team_leader = request.POST.get('common_password_team_leader')

        leader_names = request.POST.getlist('leader_name')
        emails = request.POST.getlist('email')
        phone_numbers = request.POST.getlist('phone_number')
        print(leader_names)
        print(emails)
        print(phone_numbers)
        for i in range(len(leader_names)):
            form_data = {
                'leader_name': leader_names[i],
                'email': emails[i],
                'phone_number': phone_numbers[i],
                'common_password_team_leader': common_password_team_leader,
            }

            team_leader_form = TeamLeaderDetailsForm(form_data)
            
            if team_leader_form.is_valid():
                team_leader = team_leader_form.save(commit=False)
                team_leader.rescue_agency = rescue_agency
                team_leader.profile = request.user.profile
                team_leader.save()
                user = User.objects.create(username=leader_names[i])
                team_leader.user = user
                team_leader.save()
                role, created = Role.objects.get_or_create(role='rescue_agency_team_leader')
                team_leader.role = role
                team_leader.save()
                group, created = Group.objects.get_or_create(name=role.get_group_name())
                user.groups.add(group)
                user.save()
                password = form_data['common_password_team_leader']
                print(password)
                user.set_password(password)
                user.save()
                profile = Profile.objects.create(user=user)
                role, created = Role.objects.get_or_create(role='rescue_agency_team_leader') 
                profile.role = role
                profile.rescue_agency = rescue_agency
                profile.save()
                
            else:
                print(team_leader_form.errors)

        TeamLeaderCount.objects.all().delete()
        team_members_count = rescue_agency.team_member_count
        for x in range(team_members_count):
            member=TeamMemberCount.objects.create(name="name",agency=rescue_agency)
        team_member_forms = TeamMemberDetailsForm()
        count=TeamMemberCount.objects.all()
        return render(request, 'base/team_member_details.html', {'rescue_agency': rescue_agency, 'team_member_forms': team_member_forms,'team_members_count':count})

    

def save_team_member_details(request, rescue_agency_id):
    rescue_agency = RescueAgency.objects.get(id=rescue_agency_id)
    print(request.POST)
    
    if request.method == 'POST':
        common_password_team_member = request.POST.get('common_password_team_member')
        member_names = request.POST.getlist('member_name')
        emails = request.POST.getlist('email')
        phone_numbers = request.POST.getlist('phone_number')
        
        for i in range(len(member_names)):
            form_data = {
                'member_name': member_names[i],
                'email': emails[i],
                'phone_number': phone_numbers[i],
                'common_password_team_member': common_password_team_member,
            }

            team_member_form = TeamMemberDetailsForm(form_data)
            
            if team_member_form.is_valid():
                team_member = team_member_form.save(commit=False)
                team_member.rescue_agency = rescue_agency
                team_member.profile = request.user.profile 
                team_member.save()
                user = User.objects.create(username=member_names[i])
                team_member.user = user
                team_member.save()
                role, created = Role.objects.get_or_create(role='rescue_agency_team_member')
                team_member.role = role
                team_member.save()
                group, created = Group.objects.get_or_create(name=role.get_group_name())
                user.groups.add(group)
                user.save()
                password = team_member_form.cleaned_data['common_password_team_member']
                print(password)
                user.set_password(password)
                user.save()
                # Create profile of team member
                profile = Profile.objects.create(user=user)
                profile.role = role
                profile.rescue_agency = rescue_agency
                profile.save()
            else:
                print(team_member_form.errors)

        TeamMemberCount.objects.all().delete()

        return render(request, 'base/home.html')

        


def user_login(request):    
    if request.method == 'POST':
        form = SimpleLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            username = username.strip()
            user = User.objects.filter(username=username).first()
            print(user)
            if user is not None:
                print("Provided password:", password)
                user = authenticate(request, username=username, password=password)
                print("User object:", user)

                if user is not None:
                    print("Founded")
                    login(request, user)
                    return redirect('dashboard')
                else:
                    print("Authentication failed")
            else:
                print("User not found")
                return render(request, 'base/home.html', {'form': form, 'error_message': 'Invalid login credentials'})
    else:
        form = SimpleLoginForm()

    return render(request, 'base/login.html', {'form': form})


@login_required
def dashboard(request):
    try:
        user_profile = get_object_or_404(Profile, user=request.user)
        agency = user_profile.rescue_agency
        role = user_profile.role
        print(agency)
        agency_latitude = agency.latitude if agency else None
        agency_longitude = agency.longitude if agency else None
        all_agencies = RescueAgency.objects.all()

        context = {
            'user_role': role.role,
            'user_agency': agency.organization_name if agency else None,
            'agency_latitude': agency_latitude,
            'agency_longitude': agency_longitude,
            'agencies': all_agencies,
        }
        print(context)
        return render(request, 'base/dashboard.html', context)
    except Profile.DoesNotExist:
        return render(request, 'base/dashboard.html', {'error_message': 'Profile not found'})

#===============================================================================================

def view_rescue_agency_profile(request):
    
    user_agency_name = request.GET.get('user_agency', '')
    selected_agency_name = request.GET.get('selected_agency', '')
    user_agency = get_object_or_404(RescueAgency, organization_name=user_agency_name)
    selected_agency = get_object_or_404(RescueAgency, organization_name=selected_agency_name)
    admin = get_object_or_404(TeamLeader, rescue_agency=selected_agency, is_admin=True)
    team_leaders = TeamLeader.objects.filter(rescue_agency=selected_agency, is_admin=False)
    team_members = TeamMember.objects.filter(rescue_agency=selected_agency)
    context = {
        'user_agency': user_agency,
        'selected_agency': selected_agency,
        'admin_name': admin.leader_name if admin else None,
        'team_leaders': team_leaders,
        'team_members': team_members,
    }
    return render(request, 'base/rescue_agency_profile.html', context)


def view_rescue_agency_profile(request):
    agency_name = request.GET.get('agency', '')
    rescue_agency = get_object_or_404(RescueAgency, organization_name=agency_name)
    admin_name = Profile.objects.filter(rescue_agency=rescue_agency, role__role='rescue_agency_admin').first()
    resources = Resource.objects.filter(agency=rescue_agency)
    team_leaders = TeamLeader.objects.filter(rescue_agency=rescue_agency)
    team_members = TeamMember.objects.filter(rescue_agency=rescue_agency)
    team_leader_emails = [(team_leader, team_leader.email) for team_leader in team_leaders]
    team_member_emails = [(team_member, team_member.email) for team_member in team_members]
    context = {
        'rescue_agency': rescue_agency,
        'admin_name': admin_name,
        'resources': resources,
        'team_leaders': team_leaders,
        'team_leader_emails': team_leader_emails,
        'team_members': team_members,
        'team_member_emails': team_member_emails,
    }

    return render(request, 'base/view_rescue_agency_profile.html', context)

def my_agency_details(request):
    profile = Profile.objects.get(user=request.user)
    rescue_agency = profile.rescue_agency
    admin_name = Profile.objects.filter(rescue_agency=rescue_agency, role__role='rescue_agency_admin').first()
    resources = Resource.objects.filter(agency=rescue_agency)
    team_leaders = TeamLeader.objects.filter(rescue_agency=rescue_agency)
    team_members = TeamMember.objects.filter(rescue_agency=rescue_agency)

    context = {
        'rescue_agency': rescue_agency,
        'admin_name': admin_name.user.username if admin_name else None,
        'resources': resources,
        'team_leaders': team_leaders,
        'team_members': team_members,
    }
    return render(request,'base/my_agency_details.html',context)