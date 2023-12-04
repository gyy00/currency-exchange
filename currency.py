import requests
import json
from datetime import date
from datetime import timedelta
import matplotlib.pyplot as plt
import pandas as pd


#Get data from past 30 days
#Data is limited to once every 5 days due to free subscription limits
def getHist(today):
    hist = {'Date':[],
            'USD': [],
            'EUR': []}
    
    today = date.today()
    yesterday = today - timedelta(days = 1)

    
    for i in range(7):
        if i == 0:
            day = str(today - timedelta(days = 1))
        else:
            day = str(today - timedelta(days = 5*i))
        hist['Date'].append(day)

        #Data from https://app.freecurrencyapi.com/
        data_url = 'https://api.currencyapi.com/v3/historical?apikey=fca_live_p0TopWEyEj0qqAgOYzV4U2hsHwryEwAYwDmrVEO1&currencies=USD%2CEUR&base_currency=GBP&date='+day
        response = requests.get(data_url)
        rate = json.loads(response.text)
        hist['USD'].append(rate['data']['USD']['value'])
        hist['EUR'].append(rate['data']['EUR']['value'])
    return hist


def main():
    today = date.today()
    data = getHist(today)

    #Example data
##    data = {'Date': ['2023-12-03', '2023-11-29', '2023-11-24', '2023-11-19', '2023-11-14', '2023-11-09', '2023-11-04'],
##    'USD': [1.2715041358, 1.2693896922, 1.2604457551, 1.2451747705, 1.249234694, 1.2216871693, 1.2375163123],
##    'EUR': [1.1674444161, 1.1566933975, 1.1520601554, 1.1417755913, 1.1479968824, 1.1451242008, 1.1527342115]}

    #Create pandas dataframe
    df = pd.DataFrame.from_dict(data)

    x = df['Date']
    y1 = df['USD']
    y2 = df['EUR']

    #Create a single figure and axes
    fig, ax = plt.subplots()

    #Plot both data sets on the same axes
    ax.plot(x, y1, color='blue', label='USD')
    ax.plot(x, y2, color='red', label='EUR')

    #Adjust layout so that the date fits within the window
    plt.subplots_adjust(bottom=0.25)

    #Set labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Exchange Rate')
    ax.set_title('USD/EUR Exchange Rates from GBP')
    ax.legend()
    
    #Rotate dates on the x axis
    plt.xticks(rotation=90)

    #show plot
    plt.show()

    

main()
