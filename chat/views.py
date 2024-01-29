# chat/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from base.models import RescueAgency, Profile

@login_required
def open_chat(request):
    try:
        
        user_profile = Profile.objects.get(user=request.user)
        user_agency = user_profile.rescue_agency
    except Profile.DoesNotExist:
        
        user_agency = None

    
    messages = Message.objects.all()

    return render(request, 'chat/open_chat.html', {'user_agency': user_agency, 'messages': messages})


@login_required
def send_message(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, content=content)

    return redirect('open_chat')    