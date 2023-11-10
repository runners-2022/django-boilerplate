from django.db import models
from django.forms import Textarea

from nested_inline.admin import NestedStackedInline, NestedTabularInline

from runners.utils.inlines import ReadOnlyFieldsMixin


class TabularInline(ReadOnlyFieldsMixin, NestedTabularInline):
    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 1, "style": "width: 70%;"})},
    }


class StackedInline(ReadOnlyFieldsMixin, NestedStackedInline):
    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 1, "style": "width: 70%;"})},
    }
