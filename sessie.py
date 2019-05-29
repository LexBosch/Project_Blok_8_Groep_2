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
