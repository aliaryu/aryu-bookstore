from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


phone_numeric_validator = RegexValidator(
    regex   = r"^\d+$",
    message = _("phone number can only contain numbers")
)

phone_format_validator = RegexValidator(
    regex   = r"^09\d{9}$",
    message = _("phone number must start with 09 and it must be 11 digits")
)
