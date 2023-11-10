# Django
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField
from django.utils.translation import gettext_lazy as _

# Fields
from runners.apps.users.models.fields import PhoneNumberField

# Managers
from runners.apps.users.models.managers.objects import UserManager

# Mixins
from runners.apps.users.models.mixins import UserImageModelMixin

# Bases
from runners.bases.models import Model


# Main Section
class User(UserImageModelMixin,
           AbstractUser,
           Model):
    name = CharField(_('이름'), null=True, blank=True, max_length=255)
    username = CharField(_('닉네임'), null=True, blank=True, max_length=255)
    email = EmailField(_('이메일'), unique=True)
    phone = PhoneNumberField(_('전화번호'), max_length=20, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = verbose_name_plural = _('유저')
        ordering = ['-created']

    def __str__(self):
        return self.email
