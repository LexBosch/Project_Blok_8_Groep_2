#author: Sophie Hospel
#date: 30-05-2019
#databaseconnectieV1.3 geupdate, alles wat nu aangepast wordt v1.4

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
    resultaatquery_sessie_tuple = []
    resultaatquery_sessie = []
    datum = "curdate()"

    query = """INSERT INTO owe7_pg1.session (Title_session, Date_session) VALUES('{0}',{1});""".format(sessie.get_titel(), datum)
    resultaat = """select last_insert_id();"""
    mycursor2 = cnx.cursor()
    mycursor2.execute(query)
    mycursor2.execute(resultaat)
    resultaatquery_sessie_tuple += mycursor2.fetchall()
    for item in resultaatquery_sessie_tuple:
        value = item[0]
        resultaatquery_sessie.append(value)
    print(resultaatquery_sessie)

    cnx.commit()
    mycursor2.close()
    tabel_search_query_vullen(sessie, resultaatquery_sessie, cnx)


def tabel_search_query_vullen(sessie, resultaatquery_sessie, cnx):
    ###search query vullen

    resultaatquery_termen_tuple = []
    resultaatquery_termen = []
    for zoekwoord in sessie.get_zoekwoorden():
        term = str(zoekwoord.get_term())
        query = """INSERT INTO owe7_pg1.search_query (Term) VALUES('{0}');""".format(term)
        resultaat = """select last_insert_id();"""
        mycursor2 = cnx.cursor()
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
    ###relatie tussen sessie en zoekterm vullen

    mycursor2 = cnx.cursor()
    for sessieid in resultaatquery_sessie:
        idSession = sessieid
        for item in set(resultaatquery_termen):
            print(item)
            query = """insert into owe7_pg1.session_has_search_query (Session_idSession, Search_query_idSearch_query) VALUES({0},{1})""".format(idSession, item)
            mycursor2.execute(query)
            cnx.commit()

    mycursor2.close()
    tabel_information_article_vullen(sessie, resultaatquery_termen, cnx)


def tabel_information_article_vullen(sessie, resultaatquery_termen, cnx):
    ###information article vullen

    resultaatquery_artikelen_tuple = []
    resultaatquery_artikelen = []
    for zoekwoord in sessie.get_zoekwoorden():
        for artikel in zoekwoord.get_artikelen():
            pubmedid = str(artikel.get_pubmed_id())
            titel = str(artikel.get_titel())
            pubdatum = str(artikel.get_pub_datum())
            query = """INSERT INTO owe7_pg1.information_article (PubMedID, Title, Year_publication) VALUES('{0}', '{1}', '{2}');""".format(pubmedid, titel, pubdatum)
            resultaat = """select last_insert_id();"""
            mycursor2 = cnx.cursor()
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
    ###relatietabel zoekterm en artikel vullen


    print(resultaatquery_termen)
    print(resultaatquery_artikelen)

    mycursor2 = cnx.cursor()
    for termnid in resultaatquery_termen:
        idSearch_query = termnid
        for item in set(resultaatquery_artikelen):
            query = """insert into owe7_pg1.information_article_has_search_query (information_article_idinformation_article, search_query_idsearch_query) VALUES({0},{1})""".format(item, idSearch_query)
            mycursor2.execute(query)
            cnx.commit()

    mycursor2.close()
    tabel_author_vullen(sessie, resultaatquery_artikelen,cnx)
    return resultaatquery_termen


def tabel_author_vullen(sessie, resultaatquery_artikelen, cnx):
    ###author vullen


    resultaatquery_author_tuple = []
    resultaatquery_author = []
    for zoekwoord in sessie.get_zoekwoord():
        for artikel in zoekwoord.get_artikelen():
            for author in artikel.get_authors():
                if not (sessie.get_insertion()):
                    tussenvoegsel = "NULL"
                else:
                    tussenvoegsel = author.get_insertion()

                query = """insert into owe7_pg1.author (Initial, Insertion, Last_name) values ( '{0}', {1}, '{2}');""".format(author.get_initial(), tussenvoegsel, author.get_last_name())
                resultaat = """select last_insert_id();"""
                mycursor1 = cnx.cursor()
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
    ###relatietabel tussen artikel en autheur vullen


    print(resultaatquery_artikelen)
    print(resultaatquery_author)

    mycursor2 = cnx.cursor()
    for value in resultaatquery_artikelen:
        idAuthor = value
        for item in resultaatquery_author:
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


def sessiesophalen(lijstid):
    cnx = connectie()
    mycursor = cnx.cursor()

    resultaatsessieID = []
    resultaatsessietitel = []
    resultaatsessiedatum = []

    for itemid in lijstid:
        resultaatsessieID_tuple = []
        queryid = """select idSession from owe7_pg1.session where idSession = {0};""".format(itemid)
        mycursor.execute(queryid)
        resultaatsessieID_tuple = mycursor.fetchall()
        for item in resultaatsessieID_tuple:
            value = item[0]
            resultaatsessieID.append(value)

        resultaatsessietitel_tuple = []
        querytitel = """select Title_session from owe7_pg1.session where idSession = {0};""".format(itemid)
        mycursor.execute(querytitel)
        resultaatsessietitel_tuple = mycursor.fetchall()
        for item in resultaatsessietitel_tuple:
            value = item[0]
            resultaatsessietitel.append(value)

        resultaatsessiedatum_tuple = []
        querydatum = """select Date_session from owe7_pg1.session where idSession = {0};""".format(itemid)
        mycursor.execute(querydatum)
        resultaatsessiedatum_tuple = mycursor.fetchall()
        for item in resultaatsessiedatum_tuple:
            value = item[0]
            resultaatsessiedatum.append(value)
        cnx.commit()

    print("IDs: ", resultaatsessieID)
    print("Titels: ", resultaatsessietitel)
    print("Datums: ", resultaatsessiedatum)

    return resultaatsessieID, resultaatsessietitel, resultaatsessiedatum


