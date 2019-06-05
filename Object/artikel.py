class Artikel(object):
    """Object article, filled with the pubmedid, title, publication date and list with author objects
    """
    def __init__(self, pubmed_id, titel, pub_datum, authors):
        """Initalyzer of the Artikel object

        :param pubmed_id: Identifier of the publication article
        :param titel: title of the publication article
        :param pub_datum: publication year of the publication article
        :param authors: list of Author objects
        """
        self.__pubmed_id = pubmed_id
        self.__titel = titel
        self.__pub_datum = pub_datum
        self.__authors = authors

    def get_pubmed_id(self):
        """
        Returns pubmed id
        :return: Pubmed id
        """
        return int(self.__pubmed_id)

    def get_titel(self):
        """
        returns pubmed title
        :return: Pubmed title
        """
        return str(self.__titel)

    def get_pub_datum(self):
        """
        Returns publication year
        :return: publication year
        """
        return int(self.__pub_datum)

    def get_authors(self):
        """
        returns list with author objects
        :return: List with Author object
        """
        return self.__authors

