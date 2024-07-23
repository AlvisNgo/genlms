def user_profile(request):
    if request.user.is_authenticated:
        profile_picture = request.user.profile.profile_picture.url if request.user.profile.profile_picture else None
        return {
            'profile_picture': profile_picture
        }
    return {}
