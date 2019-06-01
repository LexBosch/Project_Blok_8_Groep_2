import databaseconnectie


def showPage():
    print("ter")

def get_Sessions():
    """Gets all the sessionNames and dates the sessions are created

    :return: List with dictionaries with all the names and dates of the sessions
    """
    list_with_sessions = [
        {"sessionName": "sessie1 | 2019-06-01", "sesId": "1"},
        {"sessionName": "sessie2 | 2019-06-02", "sesId": "2"},
        {"sessionName": "sessie3 | 2019-06-03", "sesId": "3"},
        {"sessionName": "sessie4 | 2019-06-04", "sesId": "4"},
        {"sessionName": "sessie5 | 2019-06-05", "sesId": "5"}
    ]
    return list_with_sessions
