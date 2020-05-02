from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from jsonfield import JSONField
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



class Teachers(models.Model):
    name = models.CharField(
        blank=False,
        help_text=_("Teacher Full name, name with title should be unique, used at time time of student assigning"),
        max_length=60, 
        unique=True
    )
    designation = models.CharField(max_length=100,blank=False)
    email = models.EmailField(blank=True)
    mobile = models.CharField(max_length=30, blank=False)
    address = JSONField()

    education_history = JSONField()
    national_id = models.PositiveIntegerField(blank=True)
    previous_experience = models.CharField(max_length=500, help_text=_("teacher previous working experience"))
    
    temporary_starting_date = models.DateTimeField(auto_now_add=True)

    #salary
    recruiting_salary = models.IntegerField(
        help_text=_("Salary in BDT , at the time of recruiting")
    )
    salary_increment = models.PositiveIntegerField()
    salary_increment_date = models.DateField(auto_now_add=False)

    permanent_starting_date = models.DateTimeField(auto_now_add=False)
    additional_responsibilityHonor = models.CharField(
        help_text=_("additional work beside his/her owned work"),
        blank=True,
        max_length=300
    )
    additional_responsibilities = models.CharField(max_length=300, help_text=_("additional responsibilities , seprated"), blank=True)
    
    resigning_date = models.DateTimeField(auto_now_add=False, blank= _(""))
    commnet_about_teacher = models.TextField(
        help_text=_("Comment about the teacher from admin side, max 200 char"),
        max_length=200,
        blank=True,
    )


class students(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(help_text=_("Name for Registration(student)"),max_length=50, blank=False)
    Birth_date = models.DateField()
    father_name = models.CharField(help_text=_("Father name of student"), max_length=50, blank=False)

    #address
    present_address = JSONField(blank=True, null=True)
    permanent_address = JSONField(blank=True, null=True)
    #guardian information
    guardian_information = JSONField(blank=True, null=True)

    #examiner information 
    examiner_name = models.CharField(help_text=_("Name for examiner(student)"),max_length=50, blank=True)
    result = models.CharField(help_text=_("examiner_result"), max_length=50)
    admission_fee = models.PositiveIntegerField(_("admission fee"), blank=False, null=False)
    monthly_fee = models.PositiveIntegerField(_("student monthly fee"), blank=False)
    boarding_fee = models.PositiveIntegerField(_("student boarding fee"), blank=True, null=True)
    other_fees = JSONField(null=True)

    #additional information
    other_information = JSONField()

    #image or file  


    

    class StudentAssignmentToTeacher(models.Model):
        teacherId = models.ForeignKey(Teachers,on_delete=models.CASCADE, null=False)
        studentId = models.PositiveIntegerField(_("student unique id"))
        created_at = models.DateTimeField(default=timezone.now)
        updated_at = models.DateTimeField(_("at the time of assigning to another teacher"),default=timezone.now)

   




