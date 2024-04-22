import re
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import is_password_usable

class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"

class CustomRegexValidator(RegexValidator):
    def __call__(self, value):
        super().__call__(value)
        if len(value) < 8:
            raise ValidationError(_("Password must be at least 8 characters long."))
        if not any(char.isdigit() for char in value):
            raise ValidationError(_("Password must contain at least one digit."))
        if not any(char.islower() for char in value):
            raise ValidationError(_("Password must contain at least one lowercase letter."))
        if not any(char.isupper() for char in value):
            raise ValidationError(_("Password must contain at least one uppercase letter."))
        if not any(char in "!@#$%^&*/" for char in value):
            raise ValidationError(_("Password must contain at least one special character (!@#$%^&*/"))
            
class CustomUser(AbstractUser):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    # Regex validators
    username_validator = RegexValidator(
        regex=r'^[\w.@+-]+$',
        message="Enter a valid username.",
    )
    phone_number_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    email_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        message="Enter a valid email address.",
    )

    password_validator = CustomRegexValidator(
        regex=r'^[\w!@#$%^&*()-_+=\[\]{}|:;<>,./]+$',
        message=_("Password does not meet the requirements."),
    )

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    phone_number = models.CharField(
        _('phone number'),
        max_length=17,
        unique=True,
        validators=[phone_number_validator],
        help_text=_('Phone number must be entered in the format: \'+999999999\'. Up to 15 digits allowed.'),
        blank=True
    )
    email = models.EmailField( unique=True, validators=[email_validator])  
    password = models.CharField( max_length=128 ,validators=[password_validator]) 

    def save(self, *args, **kwargs):
        # Hash the password only if it hasn't been hashed yet
        if self.password and not is_password_usable(self.password):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
