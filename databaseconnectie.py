# author: Sophie Hospel
# date: 04-06-2019
# databaseconnectieV1.4 geupdate, alles wat nu aangepast wordt v1.5


import mysql.connector
from mysql.connector import errorcode
from Object.sessie import Session
from Object.zoekwoord import Zoekwoord
from Object.artikel import Artikel
from Object.author import Author

""" 
Connectie met database maken
Deze methode maakt de connectie die nodig zal zijn voor verdere methodes.
Return cnx: de connectie voor de database
"""


def connectie():
    try:
        cnx = mysql.connector.connect(user='owe7_pg1@hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com',
                                      password='blaat1234',
                                      host='hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com',
                                      database='owe7_pg1')
        return cnx
        cnx.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


def tabel_session_vullen(sessie):
    """Tabel sessie vullen in database
    :param sessie: vult de database met object sessie: sessie id, sessie titel en sessie datum
    :return: roept tabel_search_query_vullen aan met het object sessie,
        de lijst resultaatquery_sessie met de sessie id's en de connectie
    """

    cnx = connectie()
    resultaatquery_sessie_tuple = []
    resultaatquery_sessie = []
    datum = "curdate()"

    query = """INSERT INTO owe7_pg1.session (Title_session, Date_session) VALUES('{0}',{1});""".format(
        sessie.get_titel(), datum)
    resultaat = """select last_insert_id();"""
    mycursor2 = cnx.cursor()
    mycursor2.execute(query)
    mycursor2.execute(resultaat)
    resultaatquery_sessie_tuple += mycursor2.fetchall()
    for item in resultaatquery_sessie_tuple:
        value = item[0]
        resultaatquery_sessie.append(value)

    cnx.commit()
    mycursor2.close()
    tabel_search_query_vullen(sessie, resultaatquery_sessie, cnx)


def tabel_search_query_vullen(sessie, resultaatquery_sessie, cnx):
    """Tabel search_query vullen in database
     :param sessie: vult de database met object search_query (hier term genoemd)
     :return: roept tabel_relatie_session_search_query_vullen aan met het object sessie,
         de lijst resultaatquery_sessie met de sessie id's, de lijst resultaatquery_termen
          met de search_query id's en de connectie
     """

    mycursor2 = cnx.cursor()
    resultaatquery_termen_tuple = []
    resultaatquery_termen = []
    for zoekwoord in sessie.get_zoekwoorden():
        term = str(zoekwoord.get_term())
        query = """INSERT INTO owe7_pg1.search_query (Term) VALUES('{0}');""".format(term)
        resultaat = """select last_insert_id();"""
        mycursor2.execute(query)
        mycursor2.execute(resultaat)
        resultaatquery_termen_tuple += mycursor2.fetchall()
        for item in resultaatquery_termen_tuple:
            value = item[0]
            resultaatquery_termen.append(value)
    cnx.commit()
    mycursor2.close()

    tabel_relatie_session_search_query_vullen(sessie, resultaatquery_sessie, resultaatquery_termen, cnx)
    return resultaatquery_termen


def tabel_relatie_session_search_query_vullen(sessie, resultaatquery_sessie, resultaatquery_termen, cnx):
    """De relatie tabel tussen sessie en search_query vullen in database
     :param sessie: vult de database met de id's van de ingevoerde sessie en de ingevoerde search_query
     :return: roept tabel_information_article_vullen aan met het object sessie,
         de lijst resultaatquery_termen met de search_query id's en de connectie
     """

    mycursor2 = cnx.cursor()
    for sessieid in resultaatquery_sessie:
        idSession = sessieid
        for item in set(resultaatquery_termen):
            query = """insert into owe7_pg1.session_has_search_query (Session_idSession, Search_query_idSearch_query) VALUES({0},{1})""".format(
                idSession, item)
            mycursor2.execute(query)
    cnx.commit()
    mycursor2.close()
    tabel_information_article_vullen(sessie, resultaatquery_termen, cnx)


def tabel_information_article_vullen(sessie, resultaatquery_termen, cnx):
    """Tabel information_article vullen in database
     :param sessie: vult de database met object information_article met pubmedID's, titel van het artikel
        en het jaar van publicatie van het artikel.
     :return: roept tabel_relatie_search_query_information_article_vullen aan met het object sessie,
         de lijst resultaatquery_termen met de search_query id's, de lijst resultaatquery_artikelen
          met de information_article id's en de connectie
     """

    mycursor2 = cnx.cursor()
    resultaatquery_artikelen_tuple = []
    resultaatquery_artikelen = []
    for zoekwoord in sessie.get_zoekwoorden():
        for artikel in zoekwoord.get_artikelen():
            pubmedid = str(artikel.get_pubmed_id())
            titel = str(artikel.get_titel())
            titel = titel.replace("\'", "")
            pubdatum = str(artikel.get_pub_datum())
            query = """INSERT INTO owe7_pg1.information_article (PubMedID, Title, Year_publication) VALUES("{0}", "{1}", "{2}");""".format(
                pubmedid, titel, pubdatum)
            resultaat = """select last_insert_id();"""
            mycursor2.execute(query)
            mycursor2.execute(resultaat)
            resultaatquery_artikelen_tuple = mycursor2.fetchall()
            for item in resultaatquery_artikelen_tuple:
                value = item[0]
                resultaatquery_artikelen.append(value)

    cnx.commit()
    mycursor2.close()
    tabel_relatie_search_query_information_article_vullen(sessie, resultaatquery_termen, resultaatquery_artikelen, cnx)
    return resultaatquery_artikelen


def tabel_relatie_search_query_information_article_vullen(sessie, resultaatquery_termen, resultaatquery_artikelen, cnx):
    """De relatie tabel tussen search_query en information_article vullen in database
     :param sessie: vult de database met de id's van de ingevoerde search_query en de ingevoerde artikelen
     :return: roept tabel_author_vullen aan met het object sessie, de lijst resultaatquery_artikelen met de
     information_article id's en de connectie
     """

    mycursor2 = cnx.cursor()
    for termnid in resultaatquery_termen:
        idSearch_query = termnid
        for item in set(resultaatquery_artikelen):
            query = """insert into owe7_pg1.information_article_has_search_query (information_article_idinformation_article, search_query_idsearch_query) VALUES({0},{1})""".format(
                item, idSearch_query)
            mycursor2.execute(query)

    cnx.commit()
    mycursor2.close()
    tabel_author_vullen(sessie, resultaatquery_artikelen, cnx)
    return resultaatquery_termen


def tabel_author_vullen(sessie, resultaatquery_artikelen, cnx):
    """Tabel author vullen in database
       :param sessie: vult de database met object artikel met initialen, eventuele tussenvoegsel.
            en achternaam.
       :return: roept tabel_relatie_article_author_vullen aan met het object sessie,
           de lijst resultaatquery_artikelen met de information_article id's, de lijst
           resultaatquery_author met de author id's en de connectie
       """
    mycursor1 = cnx.cursor()
    resultaatquery_author_tuple = []
    resultaatquery_author = []
    for zoekwoord in sessie.get_zoekwoorden():
        for artikel in zoekwoord.get_artikelen():
            for author in artikel.get_authors():
                if not (author.get_insertion()):
                    tussenvoegsel = "NULL"
                else:
                    tussenvoegsel = str(author.get_insertion())
                initial = str(author.get_initial())
                last_name = str(author.get_last_name())
                query = """insert into owe7_pg1.author (Initial, Insertion, Last_name) values ( '{0}', {1}, '{2}');""".format(
                    initial, tussenvoegsel, last_name)
                resultaat = """select last_insert_id();"""
                mycursor1.execute(query)
                mycursor1.execute(resultaat)
                resultaatquery_author_tuple = mycursor1.fetchall()
                for item in resultaatquery_author_tuple:
                    value = item[0]
                    resultaatquery_author.append(value)
    cnx.commit()
    mycursor1.close()
    tabel_relatie_article_author_vullen(resultaatquery_artikelen, resultaatquery_author, cnx)


def tabel_relatie_article_author_vullen(resultaatquery_artikelen, resultaatquery_author, cnx):
    """De relatie tabel tussen information_article en author vullen in database
       :param: vult de database met de id's van de ingevoerde information_articles en de ingevoerde authors
       :return: als alle autheurs er in zijn gezet dan returnt hij vanzelf alle methodes terug naar
            het begin: de sessie.
       """

    mycursor2 = cnx.cursor()
    for artikel_id in resultaatquery_artikelen:
        for author_id in set(resultaatquery_author):
            query = """insert into owe7_pg1.author_has_information_article (author_idauthor, information_article_idinformation_article) VALUES({0},{1})""".format(
                author_id, artikel_id)
            mycursor2.execute(query)
    cnx.commit()
    mycursor2.close()


def get_session(sid, cnx):
    """ Sessie bepalen van het opgegeven ID
    :param sid: sid staat voor het opgegeven sessieID
    :param cnx: cnx is de connectie die wordt meegegeven om verbinding te maken met de database
    :return sessie: sessie object gevuld met sessie, bijhorende zoektermen, artikelen en autheurs.
    """

    query = """select * from owe7_pg1.session where idSession = {0};""".format(sid)
    mycursor2 = cnx.cursor()
    mycursor2.execute(query)
    myresult = mycursor2.fetchall()
    cnx.commit()
    mycursor2.close()

    sessie = []
    for regel in myresult:
        zoekwoorden = get_zoekwoorden(sid, cnx)
        titel = regel[1]
        datum = regel[2]
        session = Session(titel, datum, zoekwoorden)
        sessie.append(session)

    return sessie


def get_zoekwoorden(sid, cnx):
    """ Zoekwoorden bepalen van bijhorende sessie
    :param sid: sid staat voor het opgegeven sessieID
    :param cnx: cnx is de connectie die wordt meegegeven om verbinding te maken met de database
    :return zoekwoorden: zoekwoorden object gevuld met de ingevoerde zoekwoorden (search_query)
    """

    query = """select * from owe7_pg1.search_query where idSearch_query in (select Search_query_idSearch_query from owe7_pg1.session_has_search_query where Session_idSession = {0});""".format(
        sid)

    mycursor2 = cnx.cursor()
    mycursor2.execute(query)
    myresult = mycursor2.fetchall()
    cnx.commit()
    mycursor2.close()

    zoekwoorden = []
    for regel in myresult:
        artikelen = get_articelen(regel[0], cnx)
        term = regel[1]
        zoekwoord = Zoekwoord(term, artikelen)
        zoekwoorden.append(zoekwoord)

    return zoekwoorden


def get_articelen(resultaat_termen, cnx):
    """ Artikelen bepalen van bijhorende sessie
    :param resultaat_termen: in de lijst resultaat_termen staan alle id's die bij de zoekwoorden zijn ingevoerd
    :param cnx: cnx is de connectie die wordt meegegeven om verbinding te maken met de database
    :return resultaat_termen: de lijst wordt gereturned om in andere delen van de code te gebruiken
    """

    for item in resultaat_termen:
        query = """select * from owe7_pg1.information_article where idInformation_article in (select Information_article_idInformation_article from owe7_pg1.information_article_has_search_query where Search_query_idSearch_query  = {0})""".format(
            item)
        mycursor2 = cnx.cursor()
        mycursor2.execute(query)
        myresult = mycursor2.fetchall()
        cnx.commit()
        mycursor2.close()

        artikelen = []
        for regel in myresult:
            authors = get_autheurs(regel[0], cnx)
            pubmedid = regel[1]
            titel = regel[2]
            publicatiedatum = regel[3]
            artikel = Artikel(pubmedid, titel, publicatiedatum, authors)
            artikelen.append(artikel)

    return resultaat_termen


def get_autheurs(resultaat_artikelen, cnx):
    """ Autheurs bepalen van bijhorende sessie
    :param resultaat_artikelen: in de lijst resultaat_artikelen staan alle id's die bij de artikelen zijn ingevoerd
    :param cnx: cnx is de connectie die wordt meegegeven om verbindning te maken met de database
    :return authors: authors object gevuld met de ingevoerde autheurs
    """

    print("resultaat artikelen:", resultaat_artikelen)
    artikel_id = resultaat_artikelen

    query = """select * from owe7_pg1.author where idAuthor in (select Author_idAuthor from owe7_pg1.author_has_information_article where Information_article_idInformation_article = {0})""".format(
        artikel_id)

    mycursor2 = cnx.cursor()
    mycursor2.execute(query)
    myresult = mycursor2.fetchall()
    cnx.commit()
    mycursor2.close()

    authors = []
    for regel in myresult:
        initial = regel[1]
        insertion = regel[2]
        last_name = regel[3]
        author = Author(initial, insertion, last_name)
        authors.append(author)

    return authors


def databasevullen(sessie):
    """ Methode die alle functies aanroept zodat de database gevuld wordt
    :param sessie: het object met alle bijhorende informatie van de sessie
    :return: Roept tabel_session_vullen aan met het object om de database te vullen
    """
    tabel_session_vullen(sessie)


def databaseophalen(id, resultaat_termen, resultaat_artikelen):
    """ Methode om de gegevens vanuit de database te halen en in het object sessie te zetten
    :param id: sessie id wat kan worden meegegeven
    :param resultaat_termen: lijst met alle id's van de ingevoerde search_querys/zoektermen
    :param resultaat_artikelen: lijst met alle id's van de ingevoerde artikelen
    :return: object sessie
    """
    cnx = connectie()
    sessie = get_session(id, cnx)
    get_zoekwoorden(id, cnx)
    get_articelen(resultaat_termen, cnx)
    get_autheurs(resultaat_artikelen, cnx)
    return sessie


def sessiesophalen():
    """ Methode om de sessie op te halen. Wordt gebruikt voor het keuzemenu bij de graph
    :return: geeft het id van de sessie terug, de titel van de sessie en de datum van de sessie. Dit wordt
        gedaan bij alle sessies in de database.
    """
    cnx = connectie()
    mycursor = cnx.cursor()

    new = """SELECT t.* FROM owe7_pg1.session t LIMIT 30;"""
    mycursor.execute(new)
    resultaatsessieID_tuple = mycursor.fetchall()
    resultaatsessieID = []
    resultaatsessietitel = []
    resultaatsessiedatum = []
    for session in resultaatsessieID_tuple:
        resultaatsessieID.append(session[0])
        resultaatsessietitel.append(session[1])
        resultaatsessiedatum.append(session[2])
    cnx.commit()

    print("IDs: ", resultaatsessieID)
    print("Titels: ", resultaatsessietitel)
    print("Datums: ", resultaatsessiedatum)

    return resultaatsessieID, resultaatsessietitel, resultaatsessiedatum
