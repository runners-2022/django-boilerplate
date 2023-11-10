# Bases
from runners.bases.api.serializers import ModelSerializer

# Models
from runners.apps.users.models import User


# Main Section
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
