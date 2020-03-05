import datetime
import time
from sqlalchemy import func, cast, DATE


from .. import db
from ..models import Coin_Master, Coin_Current_Data, Coin_Daily_Data, Coin_Weekly_Data, Coin_Monthly_Data, Coin_History
from . coinmarketcap import fetch_tickers
from . cryptocompare import get_price, daily_price_historical, get_historical_price_per_minute



def sync_db_with_coin_data(app):

    with app.app_context():
        for coin in fetch_tickers():

            # Update Coin Master Table (if Required)
            if (Coin_Master.query.filter_by(symbol=coin['symbol']).count()) < 1:
                coin_rec = Coin_Master(name = coin['name'], symbol = coin['symbol'])
                db.session.add(coin_rec)
                print coin['symbol']
            db.session.commit()


            # Update Coin_Current_Data
            if (Coin_Current_Data.query.filter_by(symbol=coin['symbol']).count()) < 1:

                coin_rec = Coin_Current_Data(
                        symbol = coin['symbol'],
                        last_updated = datetime.datetime.fromtimestamp(int(coin['last_updated'])).strftime('%Y-%m-%d %H:%M:%S'),
                        coin_rank = coin['rank'],
                        price_usd = coin['price_usd'],
                        price_btc = coin['price_btc'],
                        percentage_change_7d = coin['percent_change_7d'],
                        percentage_change_24h = coin['percent_change_24h'],
                        percentage_change_1h = coin['percent_change_1h'],
                        volume_usd_24h = coin['24h_volume_usd'],
                        market_cap_usd = coin['market_cap_usd'],
                        max_supply = coin['max_supply'],
                        total_supply = coin['total_supply'],
                        available_supply = coin['available_supply']
                        )
                db.session.add(coin_rec)
            else:

                coin_rec =  dict(symbol = coin['symbol'],
                        last_updated = datetime.datetime.fromtimestamp(int(coin['last_updated'])).strftime('%Y-%m-%d %H:%M:%S'),
                        coin_rank = coin['rank'],
                        price_usd = coin['price_usd'],
                        price_btc = coin['price_btc'],
                        percentage_change_7d = coin['percent_change_7d'],
                        percentage_change_24h = coin['percent_change_24h'],
                        percentage_change_1h = coin['percent_change_1h'],
                        volume_usd_24h = coin['24h_volume_usd'],
                        market_cap_usd = coin['market_cap_usd'],
                        max_supply = coin['max_supply'],
                        total_supply = coin['total_supply'],
                        available_supply = coin['available_supply'])

                rows_changed = Coin_Current_Data.query.filter_by(symbol=coin['symbol']).update(coin_rec)


        db.session.commit()




def sync_coin_daily_data(app):
	with app.app_context():
		
		# Fetch Current Data
		current_data = Coin_Current_Data.query.all()

		for coin_data in current_data:
			daily_coin_rec = Coin_Daily_Data(
    			symbol = coin_data.symbol,
    			name = coin_data.name,
    			coin_rank = coin_data.coin_rank,
    			price_usd = coin_data.price_usd,
    			price_btc = coin_data.price_btc,
    			volume_usd_24h = coin_data.volume_usd_24h,
    			market_cap_usd = coin_data.market_cap_usd,
    			available_supply = coin_data.available_supply,
    			total_supply = coin_data.total_supply,
    			max_supply = coin_data.max_supply,
    			percentage_change_1h = coin_data.percentage_change_1h,
    			percentage_change_24h = coin_data.percentage_change_24h,
    			percentage_change_7d = coin_data.percentage_change_7d,
    			update_date_time = coin_data.last_updated
    			)

			db.session.add(daily_coin_rec)

		# Commit Changes to DB
		db.session.commit()



def sync_coin_weekly_data(app):
	with app.app_context():
		
		# Fetch Current Data
		current_data = Coin_Current_Data.query.all()

		for coin_data in current_data:
			daily_coin_rec = Coin_Weekly_Data(
    			symbol = coin_data.symbol,
    			name = coin_data.name,
    			coin_rank = coin_data.coin_rank,
    			price_usd = coin_data.price_usd,
    			price_btc = coin_data.price_btc,
    			volume_usd_24h = coin_data.volume_usd_24h,
    			market_cap_usd = coin_data.market_cap_usd,
    			available_supply = coin_data.available_supply,
    			total_supply = coin_data.total_supply,
    			max_supply = coin_data.max_supply,
    			percentage_change_1h = coin_data.percentage_change_1h,
    			percentage_change_24h = coin_data.percentage_change_24h,
    			percentage_change_7d = coin_data.percentage_change_7d,
    			update_date_time = coin_data.last_updated
    			)

			db.session.add(daily_coin_rec)

		# Commit Changes to DB
		db.session.commit()



def sync_coin_monthly_data(app):
	with app.app_context():
		
		# Fetch Current Data
		current_data = Coin_Current_Data.query.all()

		for coin_data in current_data:
			daily_coin_rec = Coin_Monthly_Data(
    			symbol = coin_data.symbol,
    			name = coin_data.name,
    			coin_rank = coin_data.coin_rank,
    			price_usd = coin_data.price_usd,
    			price_btc = coin_data.price_btc,
    			volume_usd_24h = coin_data.volume_usd_24h,
    			market_cap_usd = coin_data.market_cap_usd,
    			available_supply = coin_data.available_supply,
    			total_supply = coin_data.total_supply,
    			max_supply = coin_data.max_supply,
    			percentage_change_1h = coin_data.percentage_change_1h,
    			percentage_change_24h = coin_data.percentage_change_24h,
    			percentage_change_7d = coin_data.percentage_change_7d,
    			update_date_time = coin_data.last_updated
    			)

			db.session.add(daily_coin_rec)

		# Commit Changes to DB
		db.session.commit()



def price_sync_from_cryptocompare(app):

	with app.app_context():

		coins = (Coin_Current_Data.query
					.with_entities(Coin_Current_Data.symbol)
					.filter(Coin_Current_Data.coin_rank <= 40)
					.all())

		api_call_limiter = 0
		start_time = time.time()

		for coin in coins:
		
			#if (Coin_Current_Data.query.filter_by(symbol=coin.symbol).count()) >= 1:
			try:
				price = get_price(coin.symbol)
				coin_price_rec =  dict(
	                     price_usd = price['USD'],
	                     price_btc = price['BTC']
	                    )

				rows_changed = Coin_Current_Data.query.filter_by(symbol=coin.symbol).update(coin_price_rec)
			except:
				pass
			
			# Limit the API Calls
			api_call_limiter = api_call_limiter + 1
				
			
			#if api_call_limiter > 40:
			#	time.sleep(.2)


		elapsed_time = time.time() - start_time
		print "======================================================="
		print 
		print 'elapsed_time'
		print elapsed_time
		print 
		print "======================================================="
		db.session.commit()







def sync_historical_data(app):
    print
    print "Inside the block"
    print

    with app.app_context():

        coin_symbols = Coin_Master.query \
                        .with_entities(Coin_Master.symbol) \
                        .all()

        # Repeat for all the Coin Symbols
        for coin_symbol in coin_symbols:
            symbol = coin_symbol[0]


            # Check if there are records in table for a selected Coin
            table_data = db.session.query(func.max(Coin_History.data_date)) \
                            .filter(Coin_History.symbol==symbol) \
                            .one()

            # Table is empty, Add all records
            if table_data[0] is None:

                # Add All the Records if the DB Table is empty
                daily_price_list = daily_price_historical(symbol,'USD',all_data=True)

                for daily_price in daily_price_list:
                    coin_history_rec = Coin_History(
                                            symbol = symbol,
                                            name = symbol,
                                            high_usd =daily_price['high'],
                                            low_usd = daily_price['low'],
                                            data_date = datetime.datetime.fromtimestamp(int(daily_price['time'])).strftime('%Y-%m-%d %H:%M:%S'),
                                            close_usd = daily_price['close'],
                                            open_usd = daily_price['open']
                                            )
                    db.session.add(coin_history_rec)
                db.session.commit()

            # Table has some records, add or update accordingly
            else:

                # Find the lastest record (most recent date) in the table
                # and calculate the difference from current date
                datetime.timedelta = (datetime.datetime.now().date()) - table_data[0].date()

                # If we have a missing record for current or previous date
                if datetime.timedelta.days > 0:

                    # Fetch required data
                    daily_price_list = daily_price_historical('BTC','USD',all_data=False,limit=datetime.timedelta.days)

                    for daily_price in daily_price_list:
                        
                        # Check if record already exists
                        rec_count = Coin_History.query \
                                    .filter(cast(Coin_History.data_date, DATE)==(datetime.datetime.fromtimestamp(int(daily_price['time']))).date()) \
                                    .filter(Coin_History.symbol==symbol) \
                                    .count()

                        # IF Record already exists, Update it
                        if rec_count > 0:
                            coin_history_rec =  dict(symbol = symbol,
                                            name = symbol,
                                            high_usd =daily_price['high'],
                                            low_usd = daily_price['low'],
                                            data_date = datetime.datetime.fromtimestamp(int(daily_price['time'])).strftime('%Y-%m-%d %H:%M:%S'),
                                            close_usd = daily_price['close'],
                                            open_usd = daily_price['open'])

                            # Update Record
                            updated_rec = Coin_History.query \
                                .filter(cast(Coin_History.data_date, DATE)==(datetime.datetime.fromtimestamp(int(daily_price['time']))).date()) \
                                .filter(Coin_History.symbol==symbol) \
                                .update(coin_history_rec)

                        # Rec doesn't exist, Create it
                        else:
                            coin_history_rec = Coin_History(
                                            symbol = symbol,
                                            name = symbol,
                                            high_usd =daily_price['high'],
                                            low_usd = daily_price['low'],
                                            data_date = datetime.datetime.fromtimestamp(int(daily_price['time'])).strftime('%Y-%m-%d %H:%M:%S'),
                                            close_usd = daily_price['close'],
                                            open_usd = daily_price['open']
                                            )
                            db.session.add(coin_history_rec)
                    db.session.commit()





def sync_historical_data_per_minute(app):

    with app.app_context():
        coin_symbols = Coin_Master.query \
                        .with_entities(Coin_Master.symbol) \
                        .all()


        # Repeat for all the Coin Symbols
        for coin_symbol in coin_symbols:
            symbol = coin_symbol[0]


            # Add All the Records if the DB Table is empty
            daily_price_list = get_historical_price_per_minute(symbol,'USD',all_data=False,limit=1488)

            query = Coin_Daily_Data.query.filter(Coin_Daily_Data.symbol==symbol)
            query.delete()
            db.session.commit()

            for daily_price in daily_price_list:
                daily_coin_rec = Coin_Daily_Data(
                                symbol = symbol,
                                name = symbol,
                                price_usd = daily_price['close'],
                                update_date_time = datetime.datetime.fromtimestamp(int(daily_price['time'])).strftime('%Y-%m-%d %H:%M:%S')
                                )
                db.session.add(daily_coin_rec)
            db.session.commit()

            print 
            print "Done..."
            print


