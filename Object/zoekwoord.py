class Zoekwoord(object):
    """
    Zoekwoord object of the users session
    """
    def __init__(self, term, artikelen, synonymen):
        """
        Initialyzes the Zoekwoord object
        :param term: Term of the search term
        :param artikelen: List with articles of the Search term
        :param synonymen: List with synonyms of the search term
        """
        self.__term = term
        self.__artikelen = artikelen
        self.__synonymen = synonymen

    def get_term(self):
        """
        returns search term
        :return: serach term
        """
        return str(self.__term)

    def get_artikelen(self):
        """
        returns list of artikcle object
        :return: list of article object
        """
        return self.__artikelen

    def get_synonyms(self):
        """
        return list of synonyms
        :return: list of synonyms
        """
        return self.__synonymen


