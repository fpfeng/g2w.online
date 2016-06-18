from werkzeug.routing import BaseConverter


class ListConverter(BaseConverter):
    #  http://exploreflask.readthedocs.io/en/latest/views.html#url-converters
    def to_python(self, value):
        return value.split('+')

    def to_url(self, values):
        return '+'.join(BaseConverter.to_url(value)
                        for value in values)
