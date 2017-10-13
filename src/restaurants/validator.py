from django.core.exceptions import ValidationError

CATERGORIES = ['Mexican', 'American', 'Asian']
def validate_category(value):
    cat = value.capitalize()
    if not value in CATERGORIES and not cat in CATERGORIES:
        raise ValidationError(f'{value} is not a valid category')