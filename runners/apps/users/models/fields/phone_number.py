# Django Rest Framework
from phonenumber_field.modelfields import PhoneNumberField

# Utils
from runners.utils.validators import validate_international_phonenumber


# Main section
class PhoneNumberField(PhoneNumberField):
    default_validators = [validate_international_phonenumber]
