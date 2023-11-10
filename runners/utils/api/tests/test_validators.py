from rest_framework import serializers

import pytest

from runners.utils.api import validators
from runners.utils.api.fields import HybridImageField


@pytest.mark.unit
def test_image_non_empty(faker, ic):
    # Sample serializer class for testing only
    class Serializer(serializers.Serializer):
        image = HybridImageField(validators=(validators.image_non_empty,))

    # For empty image, it should raise ValidationError.
    with pytest.raises(serializers.ValidationError):
        ic(Serializer(data={"image": ""}).is_valid(raise_exception=True))

    # For non-empty, shouldn't raise error.
    try:
        sample_base64_image = "R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="
        ic(Serializer(data={"image": sample_base64_image}).is_valid(raise_exception=True))
    except Exception as exc:
        pytest.fail("Shouldn't raise exception but got: {!r}".format(exc))
