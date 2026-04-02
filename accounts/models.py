from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    profile_image = models.ImageField(
        upload_to="images/", null=True, blank=True, default="default_image.webp"
    )
    address = models.TextField(null=True, blank=True)
    phone_validator = RegexValidator(
        regex=r"^\+?1?\d{9,15}$", message="Phone number formate must be +999999999 "
    )
    phone = models.CharField(
        validators=[phone_validator], max_length=15, blank=True, null=True
    )

    def __str__(self):
        return f"{self.username} | {self.email} "
