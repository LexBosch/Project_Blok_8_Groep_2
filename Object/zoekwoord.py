class Zoekwoord(object):
    def __init__(self, term, artikelen, synonymen):
        self.__term = term
        self.__artikelen = artikelen
        self.__synonymen = synonymen

    def get_term(self):
        return str(self.__term)

    def get_artikelen(self):
        return self.__artikelen

    def get_synonyms(self):
        return self.__synonymen


