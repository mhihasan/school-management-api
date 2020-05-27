from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex=r"^\+?\d{9,15}$",
    message="Phone number must be entered in the format: '+999999999'. "
    "9 to 15 digits allowed.",
)
