#author: Sophie Hospel
#date: 30-05-2019
#databaseconnectieV1.2

#TO DO:
#nog de tabellen aan elkaar linken
#juiste documentatie bij code zetten


import mysql.connector
from mysql.connector import errorcode
from sessie import Session
from zoekwoord import Zoekwoord
from artikel import Artikel
from author import Author


def main():

    connectie()


def connectie():

    try:
        cnx = mysql.connector.connect(user='owe7_pg1@hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com',
                                      password='blaat1234',
                                      host='hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com',
                                      database='owe7_pg1')

        tabel_session_vullen(cnx)

        sid = 1
        sessie = get_session(sid, cnx)
        print(sessie)

        cnx.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


def tabel_session_vullen(cnx):
    ###session vullen


    if not (Session.get_datum()):
        datum = "curdate()"
    else:
        datum = Session.get_datum()

    query = """INSERT INTO owe7_pg1.session (Title_session, Date_session) VALUES('{0}',{1});""".format(Session.get_titel(), datum)
    resultaat = """select last_insert_id();"""
    mycursor2 = cnx.cursor()
    mycursor2.execute(query)
    resultaatquery_sessie = mycursor2.execute(resultaat)
    cnx.commit()
    mycursor2.close()
    print(resultaatquery_sessie)
    tabel_search_query_vullen(resultaatquery_sessie, cnx)


def tabel_search_query_vullen(resultaatquery_sessie, cnx):
    ###search query vullen

    query = """INSERT INTO owe7_pg1.search_query (Term) VALUES('{0}');""".format(Zoekwoord.get_term())
    resultaat = """select last_insert_id();"""
    mycursor2 = cnx.cursor()
    mycursor2.execute(query)
    resultaatquery_termen = mycursor2.execute(resultaat)
    cnx.commit()
    mycursor2.close()
    print(resultaatquery_termen)

    tabel_relatie_session_search_query_vullen(resultaatquery_sessie, resultaatquery_termen, cnx)
    #tabel_information_article_vullen(resultaatquery_termen, cnx)


def tabel_relatie_session_search_query_vullen(resultaatquery_sessie, resultaatquery_termen, cnx):
    print(resultaatquery_sessie)
    print(resultaatquery_termen)
    tabel_information_article_vullen(resultaatquery_termen, cnx)



def tabel_information_article_vullen(resultaatquery_termen, cnx):
    ###information article vullen

    query = """INSERT INTO owe7_pg1.information_article (PubMedID, Title, Year_publication) VALUES({0}, '{1}', {2});""".format(Artikel.get_pubmed_id(), Artikel.get_titel(), Artikel.get_pub_datum())
    resultaat = """select last_insert_id();"""
    mycursor2 = cnx.cursor()
    mycursor2.execute(query)
    resultaat_artikelen = mycursor2.execute(resultaat)
    cnx.commit()
    mycursor2.close()
    tabel_relatie_search_query_information_article_vullen(resultaatquery_termen, resultaat_artikelen, cnx)


def tabel_relatie_search_query_information_article_vullen(resultaat_termen, resultaat_artikelen, cnx):
    print(resultaat_termen)
    print(resultaat_artikelen)
    tabel_author_vullen(resultaat_artikelen,cnx)


def tabel_author_vullen(resultaat_artikelen, cnx):
    ###author vullen

    if not (Author.get_insertion()):
        tussenvoegsel = "NULL"
    else:
        tussenvoegsel = Author.get_insertion()
        #tussenvoegsel = voorbeeldlijst_author["Insertion"] = "'[0]'".format(voorbeeldlijst_author["Insertion"])

    query = """insert into owe7_pg1.author (Initial, Insertion, Last_name) values ( '{0}', {1}, '{2}');""".format(Author.get_initial(), tussenvoegsel, Author.get_last_name())
    resultaat = """select last_insert_id();"""
    mycursor1 = cnx.cursor()
    mycursor1.execute(query)
    resultaat_authors = mycursor1.execute(resultaat)
    cnx.commit()
    mycursor1.close()
    tabel_relatie_article_author_vullen(resultaat_artikelen, resultaat_authors, cnx)


def tabel_relatie_article_author_vullen(resultaat_artikelen, resultaat_authors, cnx):
    print(resultaat_artikelen)
    print(resultaat_authors)


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

    return zoekwoorden, sid

def get_articelen(search_id, cnx):

    query = """select * from owe7_pg1.information_article where idInformation_article in (select Information_article_idInformation_article from owe7_pg1.information_article_has_search_query where Search_query_idSearch_query  = {0})""".format(search_id)
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

    return artikelen, search_id

def get_autheurs(artikel_id, cnx):

    query = """select * from owe7_pg1.author where idAuthor in (select Author_idAuthor from owe7_pg1.author_has_information_article where Information_article_idInformation_article = {0})""".format(artikel_id)

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

main()