from bs4 import BeautifulSoup
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import requests
import pandas as pd
url = "https://www.worldometers.info/gdp/gdp-by-country/"
def getHtmlText(url):
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    return doc

def getData(chunk_size, url):
    doc = getHtmlText(url)
    headers = [element.text for element in doc.find_all("th")]
    data = [element.text for element in doc.find_all("td")]
    return [data[i:i+ chunk_size] for i in range(0,len(data), chunk_size)], headers
def pandas_reader(data, headers):
    df = pd.DataFrame(data=data,columns=headers)
    df["Population (2022) "] = df["Population (2022) "].str.replace(",","").astype(int)
    df["GDP (nominal, 2022) "] = df["GDP (nominal, 2022) "].str.replace(",","")
    df["GDP (nominal, 2022) "] = df["GDP (nominal, 2022) "].str.replace("$","").astype(int)
    df["GDP  per capita "] = df["GDP  per capita "].str.replace(",","")
    df["GDP  per capita "] = df["GDP  per capita "].str.replace("$","").astype(int)
    return df
def getApp():
    ans, headers = getData(chunk_size=8, url=url)
    df = pandas_reader(ans, headers)
    app = Dash(__name__)
    content = [html.H1(children="Title of the dash app"),
               dcc.Dropdown(df["Country"].unique(),"Tunisia", id="dropdown-selection"),
               dcc.Graph(id="graph-content")]
    app.layout = html.Div(content)
    return app
@callback(Output("graph-content","figure"),Input("dropdown-selection","value"))
def update_graph(value):
    ans, headers = getData(chunk_size=8, url=url)
    df = pandas_reader(ans, headers)
    dff = df[ df["Country"] == value]
    return px.bar(dff, x=headers, y=df[df["Country"] == value])

if __name__ == "__main__":
    app = getApp()
    app.run(debug=True)



