class Session(object):
    def __init__(self, titel, datum, sessie, zoekwoorden):
        self.__titel = titel
        self.__datum = datum
        self.__alles = sessie
        self.__zoekwoorden = zoekwoorden

    def get_titel(self):
        return str(self.__titel)

    def get_datum(self):
        return str(self.__datum)

    def get_alles(self):
        return self.__alles

    def get_zoekwoorden(self):
        return self.__zoekwoorden

