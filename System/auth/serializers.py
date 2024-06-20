from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from System.models import Profile,Files
from django.contrib.auth.models import User
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # You can add custom claims to the token here if needed
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if user is None:
            raise AuthenticationFailed("Incorrect username or password")

        # Assuming your user model has 'first_name' and 'last_name' fields
        refresh = self.get_token(user)
        # data.pop('refresh', None)
        # data.pop('access', None)
        data['user'] = {
            'id': user.id,
            'first_name': user.first_name,  # Corrected field name to 'first_name'
            'last_name': user.last_name,    # Corrected field name to 'last_name'
            'username': user.username,
            'email': user.email,
            # 'groups': list(user.groups.values_list('name', flat=True)),
            # 'token': str(refresh.access_token)
        }
        data['status'] = True
        data['Code'] = status.HTTP_200_OK
        return data
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }
    def validate_email(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value
    
    def create(self, validated_data):
        email = validated_data['email']
        user = User.objects.create_user(
            username=email,  # Set username to email
            email=email,
            password=validated_data['password']
        )
        return user

class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ['id', 'file']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    cv = FilesSerializer(many=True, required=False)

    class Meta:
        model = Profile
        fields = ['user', 'first_name', 'last_name', 'birthday', 'bio', 'cv']
        read_only_fields = ['age']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        cv_data = validated_data.pop('cv', [])
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        profile = Profile.objects.create(user=user, **validated_data)
        for cv_item in cv_data:
            file_instance = Files.objects.create(**cv_item)
            profile.cv.add(file_instance)
        return profile
    

class ProfileDetailSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(read_only=True)
    profile_picture = serializers.ImageField(source='profile_pic', read_only=True)
    cv = FilesSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'birthday', 'age', 'profile_picture', 'cv']