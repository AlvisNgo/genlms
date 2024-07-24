from django.shortcuts import redirect, render
from lms.forms import ProfileForm
from lms.models import Profile
from lms.utils import generate_sas_url

def profile_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if profile.profile_picture:
        profile.profile_picture.sas_url = generate_sas_url(profile.profile_picture.name)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            print(f"Redirecting to profile: {profile}")
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form, 'profile': profile, 'user': user})