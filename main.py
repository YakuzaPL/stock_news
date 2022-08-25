from os import environ
import requests
import smtplib
import os

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHA_VANTAGE_API_KEY=environ.get('ALPHA_VANTAGE_API_KEY')


STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = environ.get('NEWS_API_KEY')

SENDER_EMAIL = "januszprogramingu@gmail.com"

MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

jakub = "jakub.zajfert@gmail.com"


## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_params={
    "function": "TIME_SERIES_INTRADAY",
    "symbol": STOCK_NAME,
    "interval": "60min",
    "apikey": ALPHA_VANTAGE_API_KEY
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (60min)"]
data_list=[value for (key, value) in data.items()]
yesterday_closing_price = data_list[0]["4. close"]

day_before_yesterday_closing_price =data_list[16]["4. close"]

difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))

diff_percent = (difference / float(yesterday_closing_price)) * 100

if diff_percent > 5:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "q": STOCK_NAME,
        "searchIn": "title,description,content",
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]

    formatted_article_list = [f"Subject:{article['title']}. \n\nBrief: {article['description']}"
                              for article
                              in three_articles]
    for article in formatted_article_list:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=SENDER_EMAIL, password=MAIL_PASSWORD)
            connection.sendmail(from_addr=SENDER_EMAIL, to_addrs=jakub,
                                msg=article.replace("’","'"))

