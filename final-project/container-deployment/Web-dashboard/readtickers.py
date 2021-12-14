import requests


def getCouchDBTickers():

    url = "http://129.114.27.39:30010/updated-info/_all_docs?descending=true&limit=1"

    payload={}
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic YWRtaW46Y2xvdWRoZ2g='
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    document_id = response.json()["rows"][0]["id"]


    url = "http://129.114.27.39:30010/updated-info/{}".format(document_id)

    payload={}
    headers = {
    'Authorization': 'Basic YWRtaW46Y2xvdWRoZ2g='
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    ticker_dict = response.json()["value"]
    ticker_list = list(ticker_dict)

    X = []
    Y = []

    for ticker in ticker_list:
        X.append(ticker)
        Y.append(ticker_dict[ticker])


    return X, Y

