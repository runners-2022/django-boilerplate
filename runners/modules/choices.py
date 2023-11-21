from model_utils import Choices
from django.utils.translation import gettext_lazy as _

GENDER_TYPE_CHOICES = Choices(
    ('Female', _('여성')),
    ('Male', _('남성'))
)
