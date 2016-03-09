# Validators are a way to provide reusable validation logic
# for different types of fields
# See: https://docs.djangoproject.com/en/1.7/ref/validators/

from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime

def not_future(value):
    """Raise a ValidationError if the value is in the future.
    """
    now = timezone.now()
    if now <= value:
        msg=u'value is in the future'
        raise ValidationError(msg)

def not_unauthorized_word(value):
    """Raise a ValidationError if the value is in an unauthorized word list.
    """
    unauthorized_words = ['aardwolf', 'otter', 'elephant', 'chipmunk']
    if value in unauthorized_words:
        msg=u'value is in unauthorized words'
        raise ValidationError(msg)
