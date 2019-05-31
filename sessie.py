class Session(object):
    def __init__(self, titel, datum, zoekwoorden):
        self.__titel = titel
        self.__datum = datum
        self.__zoekwoorden = zoekwoorden

    def get_titel(self):
        return self.__titel

    def get_datum(self):
        return self.__datum

    def get_zoekwoorden(self):
        return self.__zoekwoorden

    def __str__(self):
        return str(self.get_titel())

    def __int__(self):
        return int(self.get_datum())
