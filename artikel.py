import textmining
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

def Artikel_vullen(all_article_dicts):
    idLijst = []
    titelLijst = []
    pub_datumLijst = []
    authorsLijst = []

    for variabele in all_article_dicts:

        idLijst.append(variabele["ID"])
        titelLijst.append(variabele["title"])
        try:

            pub_datumLijst.append(variabele["year"])
            authorsLijst.append(variabele["Author"])
        except KeyError:
            pass


        lijstArtikelen = Artikel(idLijst, titelLijst, pub_datumLijst, authorsLijst)
        return lijstArtikelen



