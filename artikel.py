class Artikel(object):
    def __init__(self, pubmed_id, titel, pub_datum, authors):
        self.__pubmed_id = pubmed_id
        self.__titel = titel
        self.__pub_datum = pub_datum
        self.__authors = authors

    def get_pubmed_id(self):
        return self.__pubmed_id

    def get_titel(self):
        return self.__titel

    def get_pub_datum(self):
        return self.__pub_datum

    def get_authors(self):
        return self.__authors

    def __str__(self):
        return str(self.__titel)

    def __int__(self):
        return int(self.__pubmed_id, self.__pub_datum)