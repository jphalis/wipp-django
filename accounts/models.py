from __future__ import unicode_literals
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from core.models import TimeStampedModel

# Create models here.


def upload_location(instance, filename):
    return "{}/profile_pictures/{}".format(instance.username, filename)


class MyUserManager(BaseUserManager):
    def create_user(self, email=None, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        now = datetime.now()
        user = self.model(
            email=self.normalize_email(email),
            date_joined=now, last_login=now
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,  password):
        user = self.create_user(
            email=email,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email',
                              max_length=80, unique=True)
    first_name = models.CharField(max_length=50, blank=True)  # Remove blank=True when live
    last_name = models.CharField(max_length=50, blank=True)  # Remove blank=True when live
    profile_picture = models.ImageField(upload_to=upload_location, blank=True)
    phone_number = PhoneNumberField(blank=True)  # Remove blank=True when live
    is_active = models.BooleanField(_('active'), default=True)
    is_admin = models.BooleanField(_('admin'), default=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        app_label = 'accounts'

    def __unicode__(self):
        return u"{}".format(self.id)

    def get_profile_view(self):
        return reverse('profile_view', kwargs={"id": self.id})

    @cached_property
    def get_short_name(self):
        return "{}".format(self.first_name)

    @cached_property
    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    @property
    def default_profile_picture(self):
        if self.profile_picture:
            return "{}{}".format(settings.MEDIA_URL, self.profile_picture)
        return settings.STATIC_URL + 'img/default-no-profile-pic.jpg'

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin


class Driver(TimeStampedModel):
    user = models.OneToOneField(MyUser, related_name='driver')
    is_active = models.BooleanField(_('active'), default=True)
    rating = models.IntegerField(default=0, null=True)
    trips_completed = models.IntegerField(default=0, null=True)

    class Meta:
        app_label = 'accounts'

    def __unicode__(self):
        return u"{}".format(self.user.id)

    @property
    def average_rating(self):
        return self.rating / self.trips_completed
