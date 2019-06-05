class Session(object):
    """
    Class object of the users sessino
    """

    def __init__(self, titel, datum, zoekwoorden):
        """
        Initialyzes the Sessie object
        :param titel: Title of the session
        :param datum: Date of the sessin
        :param zoekwoorden: List with zoekwoord Objects
        """
        self.__titel = titel
        self.__datum = datum
        self.__zoekwoorden = zoekwoorden

    def get_titel(self):
        """
        Returns the title of the session
        :return: title of the seesion
        """
        return str(self.__titel)

    def get_datum(self):
        """
        Returns the date of the session
        :return: date of the session
        """
        return str(self.__datum)

    def get_zoekwoorden(self):
        """
        Returns the list of zoekwoord objects of the sesison
        :return: list of zoekwoord objects
        """
        return self.__zoekwoorden
