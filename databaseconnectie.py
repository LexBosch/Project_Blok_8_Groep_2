#author: Sophie Hospel
#date: 30-05-2019
#databaseconnectieV1.2 geupdate, alles wat nu aangepast wordt v1.3

#TO DO:
#juiste documentatie bij code zetten


import mysql.connector
from mysql.connector import errorcode
from sessie import Session
from zoekwoord import Zoekwoord
from artikel import Artikel
from author import Author


def connectie():

    try:
        cnx = mysql.connector.connect(user='owe7_pg1@hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com',
                                      password='blaat1234',
                                      host='hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com',
                                      database='owe7_pg1')

        # tabel_session_vullen(cnx)
        #
        # sid = 1
        # sessie = get_session(sid, cnx)
        # print(sessie)
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
    ###session vullen


    cnx = connectie()

    if not (sessie.get_datum()):
        datum = "curdate()"
    else:
        datum = sessie.get_datum()

    query = """INSERT INTO owe7_pg1.session (Title_session, Date_session) VALUES('{0}',{1});""".format(sessie.get_titel(), datum)
    resultaat = """select last_insert_id();"""
    mycursor2 = cnx.cursor()
    mycursor2.execute(query)
    mycursor2.execute(resultaat)
    resultaatquery_sessie = mycursor2.fetchall()
    cnx.commit()
    mycursor2.close()
    print(resultaatquery_sessie)
    tabel_search_query_vullen(sessie, resultaatquery_sessie, cnx)


def tabel_search_query_vullen(sessie, resultaatquery_sessie, cnx):
    ###search query vullen


    query = """INSERT INTO owe7_pg1.search_query (Term) VALUES('{0}');""".format(sessie.get_term())
    resultaat = """select last_insert_id();"""
    mycursor2 = cnx.cursor()
    mycursor2.execute(query)
    resultaatquery_termen = mycursor2.execute(resultaat)
    cnx.commit()
    mycursor2.close()
    print(resultaatquery_termen)

    tabel_relatie_session_search_query_vullen(sessie, resultaatquery_sessie, resultaatquery_termen, cnx)
    return resultaatquery_termen


def tabel_relatie_session_search_query_vullen(sessie, resultaatquery_sessie, resultaatquery_termen, cnx):
    ###relatie tussen sessie en zoekterm vullen


    print(resultaatquery_sessie)
    print(resultaatquery_termen)

    idSession = resultaatquery_sessie
    mycursor2 = cnx.cursor()
    for item in resultaatquery_termen:
        query = """insert into owe7_pg1.session_has_search_query (Session_idSession, Search_query_idSearch_query) VALUES({0},{1})""".format(idSession, item)
        mycursor2.execute(query)
        cnx.commit()

    mycursor2.close()
    tabel_information_article_vullen(sessie, resultaatquery_termen, cnx)


def tabel_information_article_vullen(sessie, resultaatquery_termen, cnx):
    ###information article vullen

    query = """INSERT INTO owe7_pg1.information_article (PubMedID, Title, Year_publication) VALUES({0}, '{1}', {2});""".format(sessie.get_pubmed_id(), sessie.get_titel(), sessie.get_pub_datum())
    resultaat = """select last_insert_id();"""
    mycursor2 = cnx.cursor()
    mycursor2.execute(query)
    mycursor2.execute(resultaat)
    resultaat_artikelen = mycursor2.fetchall()
    cnx.commit()
    mycursor2.close()
    tabel_relatie_search_query_information_article_vullen(sessie, resultaatquery_termen, resultaat_artikelen, cnx)
    return resultaat_artikelen


def tabel_relatie_search_query_information_article_vullen(sessie, resultaat_termen, resultaat_artikelen, cnx):
    ###relatietabel zoekterm en artikel vullen


    print(resultaat_termen)
    print(resultaat_artikelen)

    mycursor2 = cnx.cursor()
    for value in resultaat_termen:
        idSearch_query = value
        for item in resultaat_artikelen:
            query = """insert into owe7_pg1.information_article_has_search_query (information_article_idinformation_article, search_query_idsearch_query) VALUES({0},{1})""".format(item, idSearch_query)
            mycursor2.execute(query)
            cnx.commit()

    mycursor2.close()
    tabel_author_vullen(sessie, resultaat_artikelen,cnx)
    return resultaat_termen


def tabel_author_vullen(sessie, resultaat_artikelen, cnx):
    ###author vullen

    if not (sessie.get_insertion()):
        tussenvoegsel = "NULL"
    else:
        tussenvoegsel = sessie.get_insertion()
        #tussenvoegsel = voorbeeldlijst_author["Insertion"] = "'[0]'".format(voorbeeldlijst_author["Insertion"])

    query = """insert into owe7_pg1.author (Initial, Insertion, Last_name) values ( '{0}', {1}, '{2}');""".format(sessie.get_initial(), tussenvoegsel, sessie.get_last_name())
    resultaat = """select last_insert_id();"""
    mycursor1 = cnx.cursor()
    mycursor1.execute(query)
    mycursor1.execute(resultaat)
    resultaat_authors = mycursor1.fetchall()
    cnx.commit()
    mycursor1.close()
    tabel_relatie_article_author_vullen(resultaat_artikelen, resultaat_authors, cnx)


def tabel_relatie_article_author_vullen(resultaat_artikelen, resultaat_authors, cnx):
    ###relatietabel tussen artikel en autheur vullen


    print(resultaat_artikelen)
    print(resultaat_authors)

    mycursor2 = cnx.cursor()
    for value in resultaat_artikelen:
        idAuthor = value
        for item in resultaat_authors:
            query = """insert into owe7_pg1.author_has_information_article (author_idauthor, information_article_idinformation_article) VALUES({0},{1})""".format(idAuthor,item)
            mycursor2.execute(query)
            cnx.commit()
    mycursor2.close()

def get_session(sid, cnx):
    ###id meegeven van sessie om die sessie met matchende andere dingen op te halen


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
        #sessie.append(session.get_titel())
        #sessie.append(session.get_datum())
        #sessie.append(zoekwoorden)

    return sessie

def get_zoekwoorden(sid, cnx):

    query = """select * from owe7_pg1.search_query where idSearch_query in (select Search_query_idSearch_query from owe7_pg1.session_has_search_query where Session_idSession = {0});""".format(sid)

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
        #zoekwoorden.append(zoekwoord.get_term())
        #zoekwoorden.append(artikelen)

    return zoekwoorden

def get_articelen(resultaat_termen, cnx):

    #deze search_id is hetzelfde als het opgehaalde getal bij tabel search query vullen

    for item in resultaat_termen:
        query = """select * from owe7_pg1.information_article where idInformation_article in (select Information_article_idInformation_article from owe7_pg1.information_article_has_search_query where Search_query_idSearch_query  = {0})""".format(item)
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
            #artikelen.append(artikel.get_pubmed_id())
            #artikelen.append(artikel.get_titel())
            #artikelen.append(artikel.get_pub_datum())
            #artikelen.append(authors)

    return resultaat_termen

def get_autheurs(resultaat_artikelen, cnx):

    artikel_id = resultaat_artikelen
    query = """select * from owe7_pg1.author where idAuthor in (select Author_idAuthor from owe7_pg1.author_has_information_article where Information_article_idInformation_article = {0})""".format(artikel_id)


    #als er meerdere artikelen ids zijn dan deze query:
    #select * from owe7_pg1.author where idAuthor in
	#   (select Author_idAuthor from owe7_pg1.author_has_information_article where Information_article_idInformation_article = 21
    #       or Information_article_idInformation_article = 1);


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
        #authors.append(author.get_initial())
        #authors.append(author.get_insertion())
        #authors.append(author.get_last_name())

    return authors


def databasevullen(sessie):
    tabel_session_vullen(sessie)


def databaseophalen(id, resultaat_termen, resultaat_artikelen):
    cnx = connectie()
    sessie = get_session(id,cnx)
    get_zoekwoorden(id, cnx)
    get_articelen(resultaat_termen, cnx)
    get_autheurs(resultaat_artikelen, cnx)
    return sessie


def sessiesophalen(id):
    cnx = connectie()
    sessie = get_session(id, cnx)
    print(str(sessie))


    return sessie


