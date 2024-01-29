# views.py
from django.shortcuts import render, redirect
from .forms import ResourceForm
import pandas as pd
from .models import Resource
from django.contrib.auth.decorators import login_required
from .forms import ResourceUploadForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .forms import ResourceForm
from .models import Resource
from base.models import Role

def is_agency_admin(user):
    return user.is_authenticated and user.profile.role == Role.objects.get(role='rescue_agency_admin')


@login_required
def upload_resources(request):
    if request.method == 'POST':
        form = ResourceUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                df = pd.read_excel(file)
                for index, row in df.iterrows():
                    name = row['Name']
                    quantity = row['Quantity']
                    Resource.objects.create(name=name, quantity=quantity, agency=request.user.profile.rescue_agency)

                messages.success(request, 'Resource data uploaded successfully.')
            except Exception as e:
                messages.error(request, f'Error reading the Excel file: {e}')

            return redirect('view_resources')
    else:
        form = ResourceUploadForm()

    return render(request, 'resources/upload_resources.html', {'form': form})

def view_resources(request):
    agency = request.user.profile.rescue_agency
    resources = Resource.objects.filter(agency=agency)

    context = {'resources': resources, 'agency': agency}
    if not resources.exists():
        if is_agency_admin(request.user):
            context['show_upload_button'] = True
            
    if is_agency_admin(request.user):
        context['updated_resources'] = True
    
    
    return render(request, 'resources/view_resources.html', context)


@user_passes_test(lambda user: user.profile.role.role == 'rescue_agency_admin')
def delete_and_upload_resources(request):
    user_agency = request.user.profile.rescue_agency
    Resource.objects.filter(agency=user_agency).delete()
    return redirect('upload_resources')

