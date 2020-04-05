from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from src.organization.models import Organization


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={"unique": _("A user with that username already exists."),},
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    is_admin_staff = models.BooleanField(
        _("admin staff status"),
        default=False,
        help_text=_("Designates whether the user is the admin of an organization."),
    )

    is_teacher = models.BooleanField(
        _("teacher status"),
        default=False,
        help_text=_("Designates whether the user is teacher."),
    )

    is_student = models.BooleanField(
        _("student status"),
        default=False,
        help_text=_("Designates whether the user is student."),
    )

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, null=True, blank=True
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)




class StudentRegistrationForm(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_name = models.CharField(name="Name for Registration(student)",max_length=50, blank=False)
    Birth_date = models.DateField()
    student_district = models.CharField(max_length=20)
    student_thana = models.CharField(max_length=20)
    student_village = models.CharField(max_length=50)
    student_optional_address = models.TextField(max_length=200, help_text="can be included post, word, house no")

    Birth_date = models.DateField()
    gaurdian_type = models.PositiveIntegerField(default=1)#one for parents 2 for others
    gaurdian_name = models.CharField(name="can be father or relative", max_length=50, blank=False)
    gaurdian_district = models.CharField(max_length=20, blank=True)
    gaurdian_thana = models.CharField(max_length=20, blank=True)
    gaurdian_village = models.CharField(max_length=50, blank=True)
    gaudian_occupation = models.CharField(max_length=40, blank=True)
    gaurdian_mobile = models.CharField(max_length=14, blank=False)
    gaurdian_optional_address = models.TextField(max_length=200,help_text="can be included post, word, house no")
    guardian_relationship = models.CharField(max_length=50, blank=False)
   




