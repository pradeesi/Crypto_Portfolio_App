from datetime import datetime

from database.db_init import session
from coinmarketcap_api import fetch_tickers
from database.db_models import Coin_Master, Coin_Current_Data

from database.db_init import session



def cmc_update_coin_master():

    for coin in fetch_tickers():

        # Update Coin Master Table (if Required)
        if (session.query(Coin_Master).filter(Coin_Master.symbol==coin['symbol']).count()) < 1:
            try:
                coin_rec = Coin_Master(name = coin['name'], symbol = coin['symbol'])
                session.add(coin_rec)
                print coin['symbol']
            except:
                pass
        session.commit()



def cmc_sync_db_with_coin_data():

    for coin in fetch_tickers():

        # Update Coin_Current_Data
        if (session.query(Coin_Current_Data).filter(Coin_Current_Data.symbol==coin['symbol']).count()) < 1:

            coin_rec = Coin_Current_Data(
                symbol=coin['symbol'],
                last_updated=datetime.fromtimestamp(int(coin['last_updated'])).strftime(
                    '%Y-%m-%d %H:%M:%S'),
                coin_rank=coin['rank'],
                price_usd=coin['price_usd'],
                price_btc=coin['price_btc'],
                percentage_change_7d=coin['percent_change_7d'],
                percentage_change_24h=coin['percent_change_24h'],
                percentage_change_1h=coin['percent_change_1h'],
                volume_usd_24h=coin['24h_volume_usd'],
                market_cap_usd=coin['market_cap_usd'],
                max_supply=coin['max_supply'],
                total_supply=coin['total_supply'],
                available_supply=coin['available_supply']
            )
            session.add(coin_rec)
        else:

            coin_rec = dict(symbol=coin['symbol'],
                            last_updated=datetime.fromtimestamp(int(coin['last_updated'])).strftime(
                                '%Y-%m-%d %H:%M:%S'),
                            coin_rank=coin['rank'],
                            price_usd=coin['price_usd'],
                            price_btc=coin['price_btc'],
                            percentage_change_7d=coin['percent_change_7d'],
                            percentage_change_24h=coin['percent_change_24h'],
                            percentage_change_1h=coin['percent_change_1h'],
                            volume_usd_24h=coin['24h_volume_usd'],
                            market_cap_usd=coin['market_cap_usd'],
                            max_supply=coin['max_supply'],
                            total_supply=coin['total_supply'],
                            available_supply=coin['available_supply'])

            session.query(Coin_Current_Data).filter(Coin_Current_Data.symbol==coin['symbol']).update(coin_rec)

    session.commit()
