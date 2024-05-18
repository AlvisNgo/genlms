from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount

def login(request):
    return render(request, 'login.html')

def student_dashboard(request):
    user = request.user
    context = {}

    if user.is_authenticated:
        social_account = SocialAccount.objects.filter(user=user, provider='microsoft').first()
        if social_account:
            extra_data = social_account.extra_data
            avatar_url = extra_data.get('photo', {}).get('url')
            context['avatar_url'] = avatar_url
    
    return render(request, 'dashboard.html', context)