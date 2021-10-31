class FourDigitYearConverter:
    regex = "[0-9]{4}"

    @staticmethod
    def to_python(value):
        return int(str(value).strip(" "))

    @staticmethod
    def to_url(value):
        return str(value).strip(" ")
