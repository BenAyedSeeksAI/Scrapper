from bs4 import BeautifulSoup
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
    

ans, headers = getData(chunk_size=8, url=url)
print(headers)
df = pandas_reader(ans, headers)
print(df[df["Country"] == "Tunisia"])



