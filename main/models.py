# -*- coding: utf-8 -*-
import random

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from utils.mobizonproxy import send_sms


class MyUserManager(BaseUserManager):
    """
    Custom user manager.
    """

    def create_user(self, email, password):
        """
        Creates and saves a User with the given email and password
        """
        if not email or not password:
            raise ValueError('Users must have an email and password')

        user = self.model(email=email.lower())
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password
        """
        user = self.create_user(email=email,
                                password=password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with email.
    """
    email = models.CharField(max_length=200, blank=False, unique=True, db_index=True)

    name = models.CharField(max_length=200, default="", blank=True, null=True, verbose_name=u'Имя')

    push_token = models.CharField(max_length=200, default="", blank=True, db_index=True)
    sound = models.BooleanField(default=True)
    sound_name = models.CharField(max_length=255, default="onesignal0")

    is_active = models.BooleanField(default=True, verbose_name=u'Активный')
    is_admin = models.BooleanField(default=False, verbose_name=u'Админ')

    timestamp = models.DateTimeField(auto_now_add=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    DEMO = 1
    PRO = 2

    TARIFFS = (
        (DEMO, u'Демо'),
        (PRO, u'PRO'),
    )

    tariff = models.SmallIntegerField(choices=TARIFFS, db_index=True, default=DEMO, verbose_name=u"Тариф")
    tariff_date = models.DateField(blank=True, null=True, verbose_name=u'Дата окончания')

    def days_left(self):
        if self.tariff_date:
            days = ((self.tariff_date - timezone.now().date()).total_seconds() / 3600) / 24
        else:
            days = 0
        if days < 0:
            days = 0
        return days

    def json(self):
        obj = {
            "user_id": self.pk,
            "phone": self.email,
            "sound": self.sound,
            "tariff": self.get_tariff_display(),
            "sound_name": self.sound_name
        }
        if self.tariff_date:
            obj["tariff_date"] = ((self.tariff_date - timezone.now().date()).total_seconds() / 3600) / 24
        else:
            obj["tariff_date"] = 0
        if obj["tariff_date"] < 0:
            obj["tariff_date"] = 0
        return obj


    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.is_admin

    @property
    def phone(self):
        """Is the user a member of staff?"""
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class TokenLog(models.Model):
    """
    Token log model
    """
    token = models.CharField(max_length=500, blank=False, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False, related_name='tokens')
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return "token={0}".format(self.token)

    class Meta:
        index_together = [
            ["token", "user"]
        ]


class ActivationManager(models.Manager):
    """
    Custom manager for Activation model
    """

    def create_code(self, phone, is_master=True):
        if phone in ["+77753721232", "+77001112233", "+77752470125", "+77074443333"]:
            code = "4512"
        else:
            code = "%0.4d" % random.randint(0, 9999)
            msms = send_sms(phone, text=u"{} - BetMates".format(code))

        activation = Activation(phone=phone,
                                code=code)
        activation.save()


class Activation(models.Model):
    """
    Stores information about activations
    """
    phone = models.CharField(max_length=100, blank=False, db_index=True)
    code = models.CharField(max_length=100, blank=False, db_index=True)
    used = models.BooleanField(default=False, db_index=True)
    objects = ActivationManager()

    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"{0} {1}".format(self.phone, self.code)

    class Meta:
        ordering = ['-timestamp']
        index_together = [
            ["phone", "used"]
        ]


class Feedback(models.Model):
    """
    Stores information about activations
    """
    message = models.TextField(max_length=2555, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False, related_name='feedbacks')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"{0} {1}".format(self.user, self.message)

    class Meta:
        ordering = ['-timestamp']
