# Django
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

# Django Rest Framework
from rest_framework.authtoken.models import Token

# Models
from runners.apps.users.models import User


# Main Section
@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    print('========== User post_save ==========')

    if created:
        # Create Token
        Token.objects.create(user=instance)


@receiver(pre_save, sender=User)
def cache_image(sender, instance, *args, **kwargs):
    print('========== User pre_save: profile_image ==========')

    profile_image = None

    if instance.id:
        user = User.objects.get(id=instance.id)
        profile_image = user.profile_image

    instance.__profile_image = profile_image


@receiver(post_save, sender=User)
def image_update(sender, instance, created, **kwargs):
    print('========== User post_save: profile_image ==========')

    if instance.__profile_image != instance.profile_image:

        # Update profile_image
        if instance.profile_image:
            instance.profile_image_url = instance.profile_image.url
            instance.save(update_fields=['profile_image_url'])
