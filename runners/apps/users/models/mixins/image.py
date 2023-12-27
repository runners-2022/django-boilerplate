# Python
import datetime

# Django
from django.db import models

# Utils
from runners.utils.medias import upload_path


# Function Section
def profile_image_path(instance, filename):
    today = datetime.date.today().strftime('%Y%m%d')
    return upload_path(f'user/{instance.uuid}/{today}/', filename)


# Main Section
class UserImageModelMixin(models.Model):
    profile_image = models.ImageField('프로필 이미지', upload_to=profile_image_path, null=True, blank=True)
    profile_image_url = models.URLField('프로필 이미지 URL', null=True, blank=True)

    class Meta:
        abstract = True
