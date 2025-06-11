from django.contrib.auth.backends import ModelBackend
from .models import MyUser  # Adjust if needed

class EmailAuthBackend(ModelBackend):  # ✅ This name MUST match settings.py
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = MyUser.objects.get(email=email)
        except MyUser.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
