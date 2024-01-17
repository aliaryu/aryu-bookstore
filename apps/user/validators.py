from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date


phone_numeric_validator = RegexValidator(
    regex = r"^\d+$",
    message = _("phone number can only contain numbers")
)

phone_format_validator = RegexValidator(
    regex = r"^09\d{9}$",
    message = _("phone number must start with 09 and it must be 11 digits")
)

birth_date_validator = MaxValueValidator(
    limit_value = date.today(),
    message = _("birth date cannot be in the future")
)
