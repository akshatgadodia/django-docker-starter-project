from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


# Custom Base User Manager
class UserManager(BaseUserManager):
    """
    Custom Manager for custom user class
    """
    def create_user(self, email, name, date_of_birth, password=None):
        """
        Method to create user
        """
        if not email:
            raise ValueError('Please provide email address')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            date_of_birth=date_of_birth
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, date_of_birth, password=None):
        """
        Method to create superuser which user create_user method and set the is_admin field to True
        """
        user = self.create_user(
            email=email,
            name=name,
            date_of_birth=date_of_birth,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# Override Base User
class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(unique=True, error_messages={'unique': 'This email already exists'})
    name = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'date_of_birth']

    def __str__(self) -> str:
        """
        Returns String Representation of User Model
        """
        return f"{self.name}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        """
        Return true if the user is admin otherwise false
        """
        return self.is_admin
        


