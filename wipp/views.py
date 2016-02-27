from django.shortcuts import render
from django.views.decorators.cache import cache_page

# Create views here.


@cache_page(60 * 60 * 24)  # 1 day: 60 sec * 60 min * 24 hours
def home(request):
    if request.user.is_authenticated():
        profile_picture = request.user.default_profile_picture
        full_name = request.user.get_full_name
        phone_number = request.user.phone_number
        context = {
            'profile_picture': profile_picture,
            'full_name': full_name,
            'phone_number': phone_number,
        }
        return render(request, 'home_visitor.html', context)
    return render(request, 'home_visitor.html', {})
