import requests
import json


COIN_MARKET_CAP_BASE_URL = "https://api.coinmarketcap.com/v1"


def fetch_global_data():
	global_data_url = COIN_MARKET_CAP_BASE_URL + "/global"
	headers = {
    	'cache-control': "no-cache",
    	}
	response = requests.request("GET", global_data_url, headers=headers)
	return json.loads(response.text)


def fetch_tickers():
	ticker_url = COIN_MARKET_CAP_BASE_URL + "/ticker"
	headers = {
    	'cache-control': "no-cache",
    	}

	response = requests.request("GET", ticker_url, headers=headers)
	return json.loads(response.text)







