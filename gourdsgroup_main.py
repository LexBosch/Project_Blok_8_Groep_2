# Autor: Lex Bosch
# Date: 25-04-2019
# WebApplication PubmedminingV0.5



from flask import Flask, render_template, request
import inputTermen
import visualiseGraph

app = Flask(__name__)
mail = "lexbosch@live.nl"


def get_datalist_element_words():
    return ["melon", "bitter melon", "Gourd", "Diabetis", "Blood suger", "Insulin", "Iron", "Magnesium", "Potassium",
            "Vitamin C", "Folic acid"]


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
                               sessionID=sessionName
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
