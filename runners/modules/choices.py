# Django
from model_utils import Choices

# Main Section
GENDER_TYPE_CHOICES = Choices(
    ('Female', '여성'),
    ('Male', '남성')
)
