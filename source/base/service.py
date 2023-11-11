from django.core.exceptions import ValidationError


def validate_size_image(file):
    megabyte_limit = 5

    if file.size > megabyte_limit*1024*1024:    
        raise ValidationError(f'File size must be less than {megabyte_limit} MB')
