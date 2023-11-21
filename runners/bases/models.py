# Python
import uuid as uuid
import timeago

# Django
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from model_utils.models import TimeStampedModel

# Third Party
from annoying.fields import AutoOneToOneField as _AutoOneToOneField


# Main Section
class AutoOneToOneField(_AutoOneToOneField):
    pass


class Manager(models.Manager):
    pass


class AvailableManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, is_deleted=False)


class UpdateMixin(object):
    def update(self, **kwargs):
        if self._state.adding:
            raise self.DoesNotExist
        for field, value in kwargs.items():
            setattr(self, field, value)
        self.save(update_fields=kwargs.keys())


class Model(UpdateMixin, TimeStampedModel, models.Model):
    is_deleted = models.BooleanField('삭제 여부', default=False, blank=True, null=True)
    deleted = models.DateTimeField('삭제 시간', blank=True, null=True)
    is_active = models.BooleanField('활성화 여부', default=True, blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    __is_deleted = None

    class Meta:
        abstract = True

    objects = Manager()
    available = AvailableManager()

    @property
    def time(self):
        return timeago.format(self.created, timezone.now(), "ko")

    def __init__(self, *args, **kwargs):
        super(Model, self).__init__(*args, **kwargs)
        self._meta.get_field("created").verbose_name = _("생성일")
        self._meta.get_field("modified").verbose_name = _("수정일")
        self.__is_deleted = self.is_deleted

    def save(self, *args, **kwargs):
        # 삭제 취소
        if self.__is_deleted != self.is_deleted and not self.is_deleted:
            self.is_deleted = False
            self.deleted = None

        return super(Model, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.is_deleted = True
        self.deleted = now()
        self.save()
