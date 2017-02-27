from django.db import models
from django.conf import settings

from djmoney.models.fields import MoneyField

from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _


class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """
    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class Administrador(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, models.CASCADE, related_name="administrador")
    nombre_empresa = models.CharField("Nombre de la empresa", max_length=32)
    slug_empresa = models.CharField(
        "ID único", max_length=64, null=True, editable=False, unique=True)


class Proyecto(models.Model):
    nombre = models.CharField(" Nombre del proyecto", max_length=64)
    descripción = models.TextField("Descripción del proyecto")
    valor_estimado = MoneyField(
        "Valor estimado del proyecto", default_currency="COP",
        decimal_places=2, max_digits=10)
    autor = models.ForeignKey(
        Administrador, models.CASCADE, related_name="proyectos")

    def __str__(self):
        return self.nombre


class Diseño(models.Model):
    EN_PROCESO = "EP"
    DISPONIBLE = "D"
    ESTADO_CHOICES = (
        (EN_PROCESO, "En proceso"),
        (DISPONIBLE, "Disponible"),
    )
    fecha_creacion = models.DateField("Fecha de creación", auto_now_add=True)
    nombres = models.CharField("Nombres", max_length=64)
    apellidos = models.CharField("Apellidos", max_length=64)
    email = models.EmailField("Correo electrónico")
    proyecto = models.ForeignKey(
        Proyecto, models.CASCADE, related_name="diseños")
    estado = models.CharField("Estado", max_length=2)
    precio_solicitado = MoneyField(
        "Precio solicitado", default_currency="COP", decimal_places=2,
        max_digits=10)
    archivo_original = models.ImageField("Diseño original")
    archivo_procesado = models.ImageField("Diseño procesado", null=True)


# Create your models here.
