from lms.utils import generate_sas_url

def user_profile(request):
    if request.user.is_authenticated:
        if request.user.profile.profile_picture:
            profile_picture = generate_sas_url(request.user.profile.profile_picture.name)
        else:
            profile_picture = None
        
        return {
            'profile_picture': profile_picture
        }
    return {}
