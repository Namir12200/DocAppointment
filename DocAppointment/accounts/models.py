from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    pic = models.ImageField(upload_to="profile_pics", default="profile_pic.png")
    is_doctor = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + " Profile"