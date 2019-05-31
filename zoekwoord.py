class Zoekwoord(object):
    def __init__(self, term, artikelen):
        self.__term = term
        self.__artikelen = artikelen

    def get_term(self):
        return self.__term

    def get_artikelen(self):
        return self.__artikelen

    def __str__(self):
        return str(self.__term)