# Autor: Lex Bosch
# Date: 25-04-2019
# WebApplication PubmedminingV0.5


import textmining
import urllib.request
from Bio import Entrez
from flask import Flask, render_template, request
import inputTermen
import visualiseGraph

app = Flask(__name__)
mail = "lexbosch@live.nl"





def get_datalist_element_words():
    return ["melon", "bitter melon", "Gourd", "Diabetis", "Blood suger", "Insulin", "Iron", "Magnesium", "Potassium",
            "Vitamin C", "Folic acid"]


# Aangeroept als de gebruiker pubmed wilt bevragen
# Input: datalist van de gebruiker met specifieke termen
# Output: render_template met de gevulde lijst
@app.route('/handle_table', methods=['POST', 'GET'])
def handle_table():
    amount_list = 3
    datalist_input = get_datalist_input(amount_list)
    papers, Zoektermen = start_PubMed_mining(datalist_input)
    new_data_dict = create_table(papers, Zoektermen)
    return render_template("BASE.html", term_list=get_datalist_element_words(),
                           amount_input=amount_list,
                           articles_list=new_data_dict,
                           pagetype="main")


# [titel, jaar, autor, id]


# Retuneerd de waardes in de datalists
# Input: het aantal datafields om te maken
# Output: Lijst met de ingevulde data uit de datalists
def get_datalist_input(amount_fields):
    new_list = []
    for x in range(0, int(amount_fields)):
        input_word = request.form['datalist{0}'.format(x + 1)]
        if input_word != "":
            new_list.append(input_word)
    return new_list


# Start het pubmed mining met een lijst met allemaal zoektermen
# Input: List met Strings van zoektermen
# Output: Lijst met de artikelen van de gevonden zoektermen
def start_PubMed_mining(term_list):
    syntax = ""
    for term in term_list:
        syntax += "{0} AND ".format(term)
    Zoektermen = syntax[0:-5]
    print(Zoektermen)
    ##print(syntax[0:-5])
    results = search(syntax[0:-5])

    id_list = results['IdList']
    papers = fetch_details(id_list)
    return papers, Zoektermen


# Details over de artikelen worden opgehaald met de IDs
# Input: List met de details van de artikelen
# Output: Lijst met de artikelen in xml vorm
def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = mail
    handle_details = Entrez.efetch(db='pubmed',
                                   retmode='xml',
                                   id=ids)
    try:
        results = Entrez.read(handle_details)["PubmedArticle"]
    except RuntimeError:
        results = "Niets gevonden"
    return results


# IDs worden opgehaald van de pubmed database aan de hand van de queries
# Input: Query met de zoektermen
# Output: Lijst met de resultaten
def search(query):
    Entrez.email = mail
    handle_search = Entrez.esearch(db='pubmed',
                                   sort='relevance',
                                   retmax='10000',
                                   retmode='xml',
                                   term=query + """ AND ("2010"[Date - Create] : "3000"[Date - Create]) AND English[Language]""")
    results = Entrez.read(handle_search)
    return results


# Parsed de artikelen in een dictionary
# Input: publicaties
# Output: Markup van de table
def create_table(publication_data, Zoektermen):
    term_list = {}
    all_article_dicts = []
    for paper in publication_data:
        if paper:
            article_dict = {}
            try:
                # PubmedIDs
                article_dict["ID"] = paper["MedlineCitation"]["PMID"]
                # Artikel data (Deze mist nogal vaak)
                article_dict["year"] = paper["MedlineCitation"]["DateCompleted"]["Year"]
                # Titel van het artikel
                article_dict["title"] = paper["MedlineCitation"]["Article"]["ArticleTitle"]
                # Authors van het artikel
                name_dict = []
                for author in paper["MedlineCitation"]["Article"]["AuthorList"]:
                    temp_name_dict = {"fore": author["Initials"], "last": author["LastName"]}
                    name_dict.append(temp_name_dict)
                article_dict["Author"] = name_dict
                # temp
                for keyword in paper['MedlineCitation']['KeywordList']:
                    for term in keyword:
                        term = term.lower()
                        if term in term_list:
                            term_list[term] += 1
                        else:
                            term_list[term] = 1
                # endtemp
            except KeyError:
                # PubmedIDs
                article_dict["ID"] = paper["MedlineCitation"]["PMID"]
                # Artikel data (Deze mist nogal vaak)
                article_dict["year"] = "Onbekend"
                # Titel van het artikel
                article_dict["title"] = paper["MedlineCitation"]["Article"]["ArticleTitle"]
                # Authors van het artikel
                name_dict = []

                # temp
                for keyword in paper['MedlineCitation']['KeywordList']:
                    for term in keyword:
                        term = term.lower()
                        if term in term_list:
                            term_list[term] += 1
                        else:
                            term_list[term] = 1
                # endtemp

                try:
                    for author in paper["MedlineCitation"]["Article"]["AuthorList"]:
                        try:
                            temp_name_dict = {"fore": author["Initials"], "last": author["LastName"]}
                            name_dict.append(temp_name_dict)
                        except KeyError:
                            temp_name_dict = {}
                except KeyError:
                    name_dict.append({"fore": "No authors found", "last": ""})
                article_dict["Author"] = name_dict
            except TypeError:
                print()
        if article_dict:
            all_article_dicts.append(article_dict)

    #

    new_data_term_list = {}

    for key in term_list:
        if term_list[key] >= 5:
            new_data_term_list[key] = term_list[key]



@app.route('/graphShown', methods=['GET'])
def graphShown():


    sessionName = request.args.get('selectSession')
    amountShow = request.args.get('selectAmount')
    if (sessionName == "-"):
        return render_template("BASE.html", term_list=get_datalist_element_words(),
                               articles_list=[],
                               pagetype="graph",
                               session_list=visualiseGraph.get_Sessions(),
                               sessionID="")
    else:
        print("SessionID:\t", sessionName)
        print("Amountshow\t", amountShow)
        return render_template("BASE.html", term_list=get_datalist_element_words(),
                               articles_list=[],
                               pagetype="graph",
                               session_list=visualiseGraph.get_Sessions(),
                               sessionID = sessionName
                            )


@app.route('/graph', methods=['POST', 'GET'])
def graph():
    # sessionName = request.form['selectSession']
    # amountShow = request.form['selectAmount']
    # if (sessionName == "-"):
    return render_template("BASE.html", term_list=get_datalist_element_words(),
                           articles_list=[],
                           pagetype="graph",
                           session_list=visualiseGraph.get_Sessions(),
                           sessionID="")
    # else:
    #     print(sessionName)
    #     print(amountShow)
    #     return render_template("BASE.html", term_list=get_datalist_element_words(),
    #                            articles_list=[],
    #                            pagetype="graph",
    #                            session_list=visualiseGraph.get_Sessions())


@app.route('/', methods=['GET', 'POST'])
def input():
    amount_list = 3
    return render_template("BASE.html",
                           amount_input=amount_list,
                           pagetype="input")


@app.route('/input_done', methods=['GET', 'POST'])
def input_done():
    amountDatalist = request.form['amountFields']
    termList = get_datalist_input(amountDatalist)
    email = request.form['emailField']
    sessionName = request.form['sessionNameField']
    amountSearch = request.form['depthSearch']
    print("termen:\t" + ", ".join(termList) +
          "\nemail:\t" + email +
          "\nsessienaam:\t" + sessionName)
    inputTermen.StartPubMedSearch(termList, sessionName, email, amountSearch)
    return render_template("BASE.html",
                           pagetype="input_done")


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template("BASE.html",
                           pagetype="about")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
