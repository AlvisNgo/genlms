from django.shortcuts import redirect, render
from lms.forms import ProfileForm
from lms.models import Profile

def profile_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            print(f"Redirecting to profile: {profile}")  # Debug statement
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    print(f"Rendering profile view for user: {user}, profile: {profile}")  # Debug statement
    return render(request, 'profile.html', {'form': form, 'profile': profile, 'user': user})


def profile_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            print(f"Redirecting to profile: {profile}")
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form, 'profile': profile, 'user': user})