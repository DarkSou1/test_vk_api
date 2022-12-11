import re

from django.core.exceptions import ValidationError


def user_phonenumber_validator(value):
    regex_phone = r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'
    if re.match(regex_phone, value) is not None:
        pass
    else:
        raise ValidationError('Введите правильно номер телефона!',
                              params={'value': value})
