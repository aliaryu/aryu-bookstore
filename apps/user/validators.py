from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date


def square_image_validator(image):
    if image.width != image.height:
        raise ValidationError(_("image must be square. width and height should be the same"))

image_extension_validator = FileExtensionValidator(
    allowed_extensions = ['jpg', 'jpeg', 'png',]
)

def postal_code_validator(value):
    if not str(value).isdigit() or len(str(value)) != 10:
        raise ValidationError(_("postal code must be a 10-digit number"))