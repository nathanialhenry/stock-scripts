from selenium import webdriver
from alpha_vantage.timeseries import TimeSeries
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
from datetime import date
import requests, time, argparse

parser = argparse.ArgumentParser()
parser.add_argument('--num',type=int, help = "Enter number of Top Daily Gainers you would like to get information on")
parser.add_argument('--key',type=str, help = "Enter Alpha Vantage API Key")
args = parser.parse_args()

# Use Selenium to scrape desired number of "Gainers" from yahoo finance for the day
driver = webdriver.Chrome("/usr/bin/chromedriver")
driver.get("https://finance.yahoo.com/gainers")
driver.implicitly_wait(10)

def getSymbols(num):
    symbols = []
    for i in range(1,num):
        symbols.append(driver.find_element_by_xpath(
        '/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[6]/div/div/section/div/div[2]/div[1]/table/tbody/tr[{0}]/td[1]/a'.format(i)).text
        )
    driver.quit()
    return symbols

# # Function for creating Today's date
# def reqDate():
#     roughDate = date.today()
#     today = roughDate.strftime("%Y-%m-%d")
#     return today

# Uses Alpha Vantage api to pull stock data from they symbols scraped from Yahoo and create charts of stock daily closing price plotted over time
def stockData(stockSymb):
    apiKey = args.key
    stockHistory = TimeSeries(apiKey, output_format = 'pandas')
    index = 0
    for symbol in stockSymb:
        stockData, metaData = stockHistory.get_daily(symbol= symbol)
        stockData['4. close'].plot()
        plt.title('Stock Price History:{0}'.format(symbol))
        plt.ylabel('price')
        plt.xlabel('time')
        index +=1
        plt.savefig('{0}: {1}.png'.format(index, symbol))
        plt.clf()
        if len(stockSymb) > 5:
            time.sleep(13)

gainersNumber = ((args.num) + 1)
stockData(getSymbols(gainersNumber))
