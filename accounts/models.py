from __future__ import unicode_literals

from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

# from phonenumber_field.modelfields import PhoneNumberField

from core.models import TimeStampedModel

# Create models here.


def upload_location(instance, filename):
    """
    Saves the uploaded file under the directory:
    'id/profile_pictures/filename'.
    """
    return "{}/profile_pictures/{}".format(instance.id, filename)


class MyUserManager(BaseUserManager):
    def create_user(self, email=None, password=None):
        """
        Creates a user in the database.
        """
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

    def create_superuser(self, email, password):
        """
        Creates a superuser in the database.
        """
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
    full_name = models.CharField(max_length=120, default='Temporary Name')
    profile_picture = models.ImageField(upload_to=upload_location, blank=True)
    # phone_number = PhoneNumberField(
    #     blank=True, help_text='When saving, format must be +1XXXXXXXXXX')
    phone_number = models.CharField(max_length=18, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_admin = models.BooleanField(_('admin'), default=False)
    is_confirmed = models.BooleanField(_('confirmed'), default=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        app_label = 'accounts'

    def __unicode__(self):
        return u"{}".format(self.full_name)

    def get_profile_view(self):
        """
        Returns the url to a user's profile.
        """
        return reverse('profile_view', kwargs={"id": self.id})

    @cached_property
    def get_short_name(self):
        """
        Returns the full name of a user.
        """
        return "{}".format(self.full_name)

    def has_module_perms(self, app_label):
        """
        Does the user have permissions to view the app `app_label`?
        """
        return True

    def has_perm(self, perm, obj=None):
        """
        Does the user have a specific permission?
        """
        return True

    @property
    def default_profile_picture(self):
        """
        Returns the profile picture of a user. If there is no profile picture,
        a default one will be rendered.
        """
        if self.profile_picture:
            return "{}{}".format(settings.MEDIA_URL, self.profile_picture)
        return settings.STATIC_URL + 'img/default-no-profile-pic.jpg'

    @property
    def is_staff(self):
        """
        Is the user a member of staff?
        """
        return self.is_admin


class Driver(TimeStampedModel):
    NEW = 0
    GOOD = 1
    FAIR = 2
    POOR = 3

    CAR_CONDITIONS = (
        (NEW, _('New')),
        (GOOD, _('Good')),
        (FAIR, _('Fair')),
        (POOR, _('Poor')),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    is_active = models.BooleanField(_('active'), default=True)
    car_make = models.CharField(max_length=30, blank=True)
    car_model = models.CharField(max_length=30, blank=True)
    car_status = models.IntegerField(
        choices=CAR_CONDITIONS, default=NEW)
    license_plate = models.CharField(max_length=12, blank=True)
    rating = models.IntegerField(default=0)
    trips_completed = models.IntegerField(default=0)

    class Meta:
        app_label = 'accounts'

    def __unicode__(self):
        return u"{}".format(self.user.full_name)

    def average_rating(self):
        """
        Returns the average rating of a driver.
        """
        if self.trips_completed > 0:
            return float("{0:.2f}".format(
                float(self.rating) / float(self.trips_completed)))
        return 0

    @cached_property
    def condition_verbose(self):
        """
        Returns the verbose of the reservation status.
        """
        return dict(Driver.CAR_CONDITIONS)[self.car_status]
