import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
import requests




def getCouchDBTickers():

    url = "http://129.114.25.83:30010/updated-info/_all_docs?descending=true&limit=1"

    payload={}
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic YWRtaW46Y2xvdWRoZ2g='
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    document_id = response.json()["rows"][0]["id"]


    url = "http://129.114.25.83:30010/updated-info/{}".format(document_id)

    payload={}
    headers = {
    'Authorization': 'Basic YWRtaW46Y2xvdWRoZ2g='
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    ticker_dict = response.json()["value"]
    ticker_list = list(ticker_dict)

    X = []
    Y = []

    for count, ticker in enumerate(ticker_list):
        if (count > 10):
            break
        X.append(ticker)
        Y.append(ticker_dict[ticker])



    return X, Y

  
app = dash.Dash(__name__)
  
app.layout = html.Div(
    [
        dcc.Graph(id = 'live-graph', animate = True),
        dcc.Interval(
            id = 'graph-update',
            interval = 3000,
            n_intervals = 0
        ),
    ]
)
  
@app.callback(
    Output('live-graph', 'figure'),
    [ Input('graph-update', 'n_intervals') ]
)


def update_graph_scatter(n):

    X, Y = getCouchDBTickers()
  
    data = plotly.graph_objs.Bar(
            x=list(X),
            y=list(Y),
            name='Bar'
    )
  
    return {'data': [data],
            'layout' : go.Layout(yaxis = dict(range = [0,max(Y)]))}
  
if __name__ == '__main__':
    app.run_server()