# Autor: Lex Bosch
# Date: 25-04-2019
# WebApplication PubmedminingV0.5


from flask import Flask, render_template, request
from Bio import Entrez

app = Flask(__name__)
mail = "lexbosch@live.nl"


@app.route('/', methods=['GET', 'POST'])
def index():
    amount_list = 3
    return render_template("BASE.html", term_list=get_datalist_element_words(),
                           amount_input=amount_list,
                           articles_list = [],
                           pagetype = "main")


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
    plz = start_PubMed_mining(datalist_input)
    new_data_dict = create_table(plz)
    return render_template("BASE.html", term_list=get_datalist_element_words(),
                           amount_input=amount_list,
                           articles_list = new_data_dict,
                           pagetype = "main")


# [titel, jaar, autor, id]


# Retuneerd de waardes in de datalists
# Input: het aantal datafields om te maken
# Output: Lijst met de ingevulde data uit de datalists
def get_datalist_input(amount_fields):
    new_list = []
    for x in range(0, amount_fields):
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
    print(syntax[0:-5])
    results = search(syntax[0:-5])
    id_list = results['IdList']
    papers = fetch_details(id_list)
    return papers


# Details over de artikelen worden opgehaald met de IDs
# Input: List met de details van de artikelen
# Output: Lijst met de artikelen in xml vorm
def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = mail
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    try:
        results = Entrez.read(handle)["PubmedArticle"]
    except RuntimeError:
        results = "Niets gevonden"
    return results


# IDs worden opgehaald van de pubmed database aan de hand van de queries
# Input: Query met de zoektermen
# Output: Lijst met de resultaten
def search(query):
    Entrez.email = mail
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax='10000',
                            retmode='xml',
                            term=query + """ AND ("2010"[Date - Create] : "3000"[Date - Create]) AND English[Language]""")
    results = Entrez.read(handle)
    return results


# Parsed de artikelen in een dictionary
# Input: publicaties
# Output: Markup van de table
def create_table(publication_data):
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
                #temp
                for keyword in paper['MedlineCitation']['KeywordList']:
                    for term in keyword:
                        term = term.lower()
                        if term in term_list:
                            term_list[term] += 1
                        else:
                            term_list[term] = 1
                #endtemp
            except KeyError:
                # PubmedIDs
                article_dict["ID"] = paper["MedlineCitation"]["PMID"]
                # Artikel data (Deze mist nogal vaak)
                article_dict["year"] = "Onbekend"
                # Titel van het artikel
                article_dict["title"] = paper["MedlineCitation"]["Article"]["ArticleTitle"]
                # Authors van het artikel
                name_dict = []


                #temp
                for keyword in paper['MedlineCitation']['KeywordList']:
                    for term in keyword:
                        term = term.lower()
                        if term in term_list:
                            term_list[term] += 1
                        else:
                            term_list[term] = 1
                #endtemp



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
                for author in paper["MedlineCitation"]["Article"]["AuthorList"]:
                    print(author["AffiliationInfo"])
                    print(author["LastName"])
        if article_dict:
            all_article_dicts.append(article_dict)

    #

    new_data_term_list = {}

    for key in term_list:
        if term_list[key] >= 3:
            new_data_term_list[key] = term_list[key]

    #


    return all_article_dicts


@app.route('/graph', methods=['GET', 'POST'])
def graph():
    amount_list = 3
    return render_template("BASE.html", term_list=get_datalist_element_words(),
                           amount_input=amount_list,
                           articles_list = [],
                           pagetype = "graph")

@app.route('/input', methods=['GET', 'POST'])
def input():
    amount_list = 3
    return render_template("BASE.html",
                           amount_input=amount_list,
                           pagetype = "input")



@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template("BASE.html",
                           pagetype = "about")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)



