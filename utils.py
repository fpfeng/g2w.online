from functools import wraps
from werkzeug.routing import BaseConverter
from flask import abort


def abort_when_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            abort(404)
    return inner


class ListConverter(BaseConverter):
    #  http://exploreflask.readthedocs.io/en/latest/views.html#url-converters
    def to_python(self, value):
        return value.split('+')

    def to_url(self, values):
        return '+'.join(BaseConverter.to_url(value)
                        for value in values)
