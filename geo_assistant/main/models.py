import re
import json
import requests

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.postgres.fields import jsonb
from django.core import validators


class MyAbstractUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=128, unique=True,
                                help_text=_('Required. 128 characters or fewer. Letters, numbers and '
                                            '@/./+/-/_ characters'),
                                validators=[
                                    validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'),
                                                              'invalid')
                                ])
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    meta = jsonb.JSONField(null=True, blank=True)

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    @property
    def name(self):
        return "%s %s" %(self.first_name, self.last_name)


class Owner(models.Model, MyAbstractUser):
    main_key = models.CharField(max_length=255)


class User(models.Model, MyAbstractUser):
    app_key = models.CharField(max_length=255)
