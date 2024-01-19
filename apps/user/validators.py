from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, FileExtensionValidator
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

def square_image_validator(image):
    if image.width != image.height:
        raise ValidationError(_("image must be square. width and height should be the same"))
    
image_extension_validator = FileExtensionValidator(
    allowed_extensions = ['jpg', 'jpeg', 'png',]
)

def postal_code_validator(value):
    if not str(value).isdigit() or len(str(value)) != 10:
        raise ValidationError(_("postal code must be a 10-digit number"))