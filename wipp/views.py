from django.shortcuts import render
from django.views.decorators.cache import cache_page

# Create views here.


@cache_page(60 * 60 * 24)  # 1 day
def home(request):
    """
    Renders the static page for when a user is signed in,
    and for a visiting user.
    """
    if request.user.is_authenticated():
        domain = request.get_host()
        profile_picture = request.user.default_profile_picture
        full_name = request.user.full_name
        phone_number = request.user.phone_number
        context = {
            'domain': domain,
            'profile_picture': profile_picture,
            'full_name': full_name,
            'phone_number': phone_number,
        }
        return render(request, 'home.html', context)
    return render(request, 'home.html', {})
