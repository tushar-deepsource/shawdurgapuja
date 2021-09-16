class FourDigitYearConverter:
    regex = '[0-9]{4}'

    def to_python(self, value):
        return int(str(value).strip(' '))

    def to_url(self, value):
        return str(value).strip(' ')
