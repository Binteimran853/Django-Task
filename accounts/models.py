from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.user_name} | {self.email}'