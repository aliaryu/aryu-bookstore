from django.core.validators import MinValueValidator, MaxValueValidator


min_percent_validator = MinValueValidator(
    limit_value = 0
)

max_percent_validator = MaxValueValidator(
    limit_value = 100
)