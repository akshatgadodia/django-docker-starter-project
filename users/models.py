from django.contrib.auth.models import AbstractUser
from django.db import models
from users.managers import UserManager


# Override Base User
class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(unique=True, error_messages={'unique': 'This email already exists'})
    name = models.CharField(max_length=200)
    date_of_birth = models.DateField()

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        """
        Returns String Representation of User Model
        """
        return f"{self.name}"
