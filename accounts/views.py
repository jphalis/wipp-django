from django.conf import settings
from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters

from .forms import (LoginForm, PasswordChangeForm,
                    RegisterForm, PasswordResetForm, SetPasswordForm)
from .models import MyUser

# Create your views here.


@sensitive_post_parameters()
@login_required
def password_change(request):
    """
    Renders a change password view for the current user.
    """
    form = PasswordChangeForm(request.POST or None, user=request.user)

    if request.method == "POST":
        if form.is_valid():
            password = form.cleaned_data['password2']
            current_user = form.user
            current_user.set_password(password)
            current_user.save()
            update_session_auth_hash(request, form.user)
            messages.success(request,
                             "You have successfully changed your password.")
    return render(request, 'accounts/settings/password_change.html',
                  {'form': form})


def password_reset(request, from_email=settings.FROM_EMAIL,
                   template_name='accounts/password_reset.html',
                   email_template_name='accounts/password_reset_email.html',
                   subject_template_name='Wipp Reset Password',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   html_email_template_name='accounts/password_reset_email.html'):
    """
    Renders a reset change password view for the current user.
    """
    if request.user.is_authenticated():
        return redirect('home')
    else:
        if request.method == "POST":
            form = password_reset_form(request.POST)
            if form.is_valid():
                opts = {
                    'use_https': request.is_secure(),
                    'token_generator': token_generator,
                    'from_email': from_email,
                    'email_template_name': email_template_name,
                    'subject_template_name': subject_template_name,
                    'request': request,
                    'html_email_template_name': html_email_template_name,
                }
                form.save(**opts)
                messages.success(request,
                                 "If that email is registered to an account, \
                                 instructions for resetting your password \
                                 will be sent soon. Please make sure to check \
                                 your junk email/spam folder if you do not \
                                 receive an email.")
        else:
            form = password_reset_form()
        return render(request, template_name, {'form': form})


@sensitive_post_parameters()
@never_cache
def password_reset_confirm(request, uidb64=None, token=None,
                           token_generator=default_token_generator):
    assert uidb64 is not None and token is not None
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = MyUser._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        form = SetPasswordForm(request.POST or None, user=user)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Password reset successfully")
                return HttpResponseRedirect(reverse("home"))
    else:
        validlink = False
        form = None
        messages.error(request, "Password reset unsuccessful")
    context = {
        'form': form,
        'validlink': validlink
    }
    return render(request, 'accounts/password_set.html', context)


def auth_logout(request):
    """
    Logs out the current user.
    """
    logout(request)
    return HttpResponseRedirect(reverse("home"))


def auth_login(request):
    """
    Logs in the user.
    """
    if request.user.is_authenticated():
        return redirect("home")
    else:
        form = LoginForm(request.POST or None)
        next_url = request.GET.get('next')

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)

                if next_url is not None:
                    return HttpResponseRedirect(next_url)
                return HttpResponseRedirect(reverse("home"))
            else:
                messages.warning(request, "Username or password is incorrect.")
        action_url = reverse("login")
        title = "Sign in"
        submit_btn = title
        context = {
            "form": form,
            "action_url": action_url,
            "title": title,
            "submit_btn": submit_btn
        }
        return render(request, 'login_register.html', context)


def auth_register(request):
    """
    Renders a view for users to register on the website.
    """
    if request.user.is_authenticated():
        return redirect("home")
    else:
        form = RegisterForm(request.POST or None)
        next_url = request.GET.get('next')

        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']
            phone_number = form.cleaned_data['phone_number']
            new_user = MyUser()
            new_user.full_name = full_name
            new_user.email = email
            new_user.set_password(password)
            new_user.phone_number = phone_number
            new_user.save()
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)

                if next_url is not None:
                    return HttpResponseRedirect(next_url)
                return HttpResponseRedirect(reverse("home"))
        action_url = reverse("register")
        title = "Register"
        submit_btn = "Create account"
        context = {
            "form": form,
            "action_url": action_url,
            "title": title,
            "submit_btn": submit_btn
        }
        return render(request, "login_register.html", context)


@sensitive_post_parameters()
@never_cache
def account_email_confirm(request, uidb64=None, token=None,
                          token_generator=default_token_generator):
    assert uidb64 is not None and token is not None
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = MyUser._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        user.is_confirmed = True
        user.save()
        messages.success(request, "Thank you for confirming your email!")
        return HttpResponseRedirect(reverse("home"))
    else:
        validlink = False
        messages.error(request, "Email confirmation unsuccessful")
    context = {
        'validlink': validlink
    }
    return render(request, 'home.html', context)
