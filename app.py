# Autor: Lex Bosch
# Date: 25-04-2019
# WebApplication PubmedminingV0.5


from flask import Flask, render_template, request
from Bio import Entrez

app = Flask(__name__)

# plz misbruik niet \o/
mail = "lexbosch@live.nl"


# index pagina van de applicatie
# input: -
# output: rendered template met de gevulde datalists
@app.route('/', methods=['GET', 'POST'])
def index():
    amount_list = 3
    return render_template("index.html", datalist_input=create_datalist(amount_list))


# Maakt element van de datalist aan
# input: list met alle woorden voor in de datalsit
# output: html markup voor alle opties van de datalist
def create_data_list_element(datalist_word_list):
    html_markup = ""
    for word in datalist_word_list:
        newstring = """<option value="{0}">""".format(word)
        html_markup += newstring
    return html_markup


# Creeërd de markup voor de datalists
# Input: Aantal datalists om aan te maken
# Output: Datalist elements met de namen "datalist" + een nummer 1 tot het aantal datalists
def create_datalist(amount_list):
    full_return = ""
    for x in range(0, amount_list):
        full_return += """
        <input list="browsers" name = "datalist{1}">
        <datalist id="browsers" name = "datalist{1}">
            {0}
        </datalist>
        """.format(create_data_list_element(get_datalist_element_words()), x + 1)
    return full_return


# Maakt de markup van de table aan met alle resultaten
# Input: publicaties
# Output: Markup van de table
def create_table(publication_data):
    new_line = ""
    for paper in publication_data:
        try:
            # PubmedIDs
            pm_id = (paper["MedlineCitation"]["PMID"])
            # Artikel data (Deze mist nogal vaak)
            year = (paper["MedlineCitation"]["Article"]["ArticleDate"][0]["Year"])
            # Titel van het artikel
            title = (paper["MedlineCitation"]["Article"]["ArticleTitle"])
            new_line += """
            <tr>
            <td>{0}</td>
            <td>{1}</td>
            <td><a href="https://www.ncbi.nlm.nih.gov/pubmed/{0}">{2}</a></td>
            <td>{3}</td>
            </tr>
            """.format(pm_id, year, title, "placeholder")
        except IndexError:
            pm_id = (paper["MedlineCitation"]["PMID"])
            year = "onbekend"
            title = (paper["MedlineCitation"]["Article"]["ArticleTitle"])
            new_line += """
            <tr>
            <td>{0}</td>
            <td>{1}</td>
            <td><a href="https://www.ncbi.nlm.nih.gov/pubmed/{0}">{2}</a></td>
            <td>{3}</td>
            </tr>
            """.format(pm_id, year, title, "placeholder")
    return new_line


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
                            retmax='20',
                            retmode='xml',
                            term=query)
    results = Entrez.read(handle)
    return results


# Start het pubmed mining met een lijst met allemaal zoektermen
# Input: List met Strings van zoektermen
# Output: Lijst met de artikelen van de gevonden zoektermen
def start_PubMed_mining(term_list):
    syntax = ""
    for term in term_list:
        syntax += "{0} AND ".format(term)
    results = search(syntax[0:-5])
    id_list = results['IdList']
    papers = fetch_details(id_list)
    return papers


# Aangeroept als de gebruiker pubmed wilt bevragen
# Input: datalist van de gebruiker met specifieke termen
# Output: render_template met de gevulde lijst
@app.route('/handle_table', methods=['POST', 'GET'])
def handle_table():
    amount_list = 3
    datalist_input = get_datalist_input(amount_list)

    newpapers = start_PubMed_mining(datalist_input)
    print()
    try:
        newtable = create_table(newpapers)
    except TypeError:
        newtable = """
                    <tr>
            <td>Geen resultaten gevonden</td>
            <td></td>
            <td></td>
            <td></td>
            </tr>
        """
    return render_template("index.html", datalist_input=create_datalist(amount_list), tableData=newtable)


# Functie die een list returnt met de termen die in de datalists moeten komen
# Input: -
# Output: List met termen die moeten worden weergeven in de datalists
def get_datalist_element_words():
    return ["melon", "bitter melon", "Gourd", "Diabetis", "Blood suger", "Insulin", "Iron", "Magnesium", "Potassium",
            "Vitamin C", "Folic acid"]


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


if __name__ == '__main__':
    app.run()
