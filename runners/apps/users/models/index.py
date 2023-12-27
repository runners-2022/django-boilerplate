# Django
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField

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
    name = CharField(verbose_name='이름', max_length=255, null=True, blank=True)
    username = CharField(verbose_name='닉네임', max_length=255, null=True, blank=True)
    email = EmailField(verbose_name='이메일', unique=True)
    phone = PhoneNumberField(verbose_name='전화번호', max_length=20, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = verbose_name_plural = '유저'
        ordering = ['-created']

    def __str__(self):
        return self.email
