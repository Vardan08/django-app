from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import MyUser, FriendRequest

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password")
        if user.block:
            raise serializers.ValidationError("User is blocked")

        data["user"] = user
        return data


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = "__all__"

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = MyUser(**validated_data)
        user.set_password(password)  # hashes password
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)  # hash new password

        instance.save()
        return instance


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'is_accepted', 'created_at']
        read_only_fields = ['sender', 'is_accepted', 'created_at']