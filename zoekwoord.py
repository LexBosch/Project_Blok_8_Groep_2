class Zoekwoord(object):
    def __init__(self, term, artikelen):
        self.__term = term
        self.__artikelen = artikelen

    def get_term(self):
        return str(self.__term)

    def get_artikelen(self):
        return self.__artikelen

