import multiprocessing
from sqlalchemy import func, cast, DATE
from datetime import datetime, timedelta

from database.db_init import session, local_db_session_for_multithreading_calls

from database.db_models import Coin_Master, CryptoCompare_Minute_History, CryptoCompare_Hourly_History, \
                        CryptoCompare_Daily_History, CryptoCompare_1hour_Chart, CryptoCompare_24hour_Chart, \
                        CryptoCompare_1week_Chart, CryptoCompare_1month_Chart, CryptoCompare_6month_Chart

from cryptocompare_api import get_daily_price_history, get_minute_price_history, get_hourly_price_history




#===============================================================
#=====  CRYPTOCOMPARE HISTORICAL API CALLS  ====================
#===============================================================

def cc_sync_minute_coin_history(no_of_workers):
    # Pull list of all the Coins
    coin_symbols = session.query(Coin_Master) \
        .with_entities(Coin_Master.symbol) \
        .all()

    if coin_symbols is not None:
        p = multiprocessing.Pool(no_of_workers)

        # Minute History
        p.map(cc_sync_minute_coin_history_thread, coin_symbols)

        p.close()
        p.join()

#===============================================================

def cc_sync_hourly_coin_history(no_of_workers):
    # Pull list of all the Coins
    coin_symbols = session.query(Coin_Master) \
        .with_entities(Coin_Master.symbol) \
        .all()

    if coin_symbols is not None:
        p = multiprocessing.Pool(no_of_workers)

        # Hourly History
        p.map(cc_sync_hourly_coin_history_thread, coin_symbols)

        p.close()
        p.join()

#===============================================================

def cc_sync_daily_coin_history(no_of_workers):
    # Pull list of all the Coins
    coin_symbols = session.query(Coin_Master) \
        .with_entities(Coin_Master.symbol) \
        .all()

    if coin_symbols is not None:
        p = multiprocessing.Pool(no_of_workers)

        # Day History
        p.map(cc_sync_daily_coin_history_thread, coin_symbols)

        p.close()
        p.join()

# ===============================================================

def cc_sync_minute_coin_history_thread(symbol_list):

    # As MySQL Community Edition doesn't support multithreading
    # we need to create a local db session for each thread
    local_session = local_db_session_for_multithreading_calls()

    symbol = symbol_list[0]
    print "Minute: " + symbol

    # Find the newest record from the CryptoCompare_1hour_Chart for a Symbol
    chart_table_rec_max_date = local_session.query(func.max(CryptoCompare_Minute_History.data_date)) \
        .filter(CryptoCompare_Minute_History.symbol == symbol) \
        .one()

    # If there is data in chart_table_rec_max_date
    if chart_table_rec_max_date[0] is not None:

        # Calculate the Minutes
        time_difference = datetime.now() - chart_table_rec_max_date[0]
        minutes_difference = divmod(time_difference.total_seconds(), 60)[0]

        # Exit the block if the data is up to date
        if minutes_difference < 1:
            print "Minute Data up to date"
            local_session.close()
            return

        # Specify the limit as the time difference (minutes) between last record and current time
        price_list_per_minute = get_minute_price_history(symbol, 'USD', all_data=False, limit=minutes_difference)

        print "Calling Minute Data API with limit: " + str(minutes_difference)
        print

    else:
        # Add All the Records if the DB Table is empty
        price_list_per_minute = get_minute_price_history(symbol, 'USD', all_data=True)

    for minute_price in price_list_per_minute:

        # Add data to the table is the Table is empty for a given Symbol or the record date is
        # greater than the max date in the Table for a given Symbol
        if (chart_table_rec_max_date[0] is None) or \
                (datetime.fromtimestamp(int(minute_price['time'])) > chart_table_rec_max_date[0]):

            #print "Adding Data for: " + symbol

            minute_coin_rec = CryptoCompare_Minute_History(
                    symbol=symbol,
                    name=symbol,
                    open_usd=minute_price['open'],
                    high_usd=minute_price['high'],
                    low_usd=minute_price['low'],
                    close_usd=minute_price['close'],
                    volume_from=minute_price['volumefrom'],
                    volume_to=minute_price['volumeto'],
                    data_date=datetime.fromtimestamp(int(minute_price['time'])).strftime('%Y-%m-%d %H:%M:%S')
                )
            local_session.add(minute_coin_rec)
    local_session.commit()
    local_session.close()


#===============================================================

def cc_sync_hourly_coin_history_thread(symbol_list):

    # As MySQL Community Edition doesn't support multithreading
    # we need to create a local db session for each thread
    local_session = local_db_session_for_multithreading_calls()

    symbol = symbol_list[0]
    print "Hourly: " + symbol

    # Find the newest record from the CryptoCompare_1hour_Chart for a Symbol
    chart_table_rec_max_date = local_session.query(func.max(CryptoCompare_Hourly_History.data_date)) \
        .filter(CryptoCompare_Hourly_History.symbol == symbol) \
        .one()

    # If there is data in chart_table_rec_max_date
    if chart_table_rec_max_date[0] is not None:

        # Calculate the Minutes
        time_difference = datetime.now() - chart_table_rec_max_date[0]
        minutes_difference = divmod(time_difference.total_seconds(), 60)[0]
        hour_difference = divmod(minutes_difference, 60)[0]


        # Exit the block if the data is up to date
        if hour_difference < 1:
            print "Hourly Data up to date"
            local_session.close()
            return

        # Specify the limit as the time difference (Hours) between last record and current time
        price_list_per_hour = get_hourly_price_history(symbol, 'USD', all_data=False, limit=hour_difference)

        print "Calling Hourly API with limit: " + str(hour_difference)
        print

    else:
        # Add All the Records if the DB Table is empty
        price_list_per_hour = get_hourly_price_history(symbol, 'USD', all_data=True)

    for hour_price in price_list_per_hour:

        # Add data to the table is the Table is empty for a given Symbol or the record date is
        # greater than the max date in the Table for a given Symbol
        if (chart_table_rec_max_date[0] is None) or \
                (datetime.fromtimestamp(int(hour_price['time'])) > chart_table_rec_max_date[0]):

            #print "Adding Data for: " + symbol

            hourly_coin_rec = CryptoCompare_Hourly_History(
                    symbol=symbol,
                    name=symbol,
                    open_usd=hour_price['open'],
                    high_usd=hour_price['high'],
                    low_usd=hour_price['low'],
                    close_usd=hour_price['close'],
                    volume_from=hour_price['volumefrom'],
                    volume_to=hour_price['volumeto'],
                    data_date=datetime.fromtimestamp(int(hour_price['time'])).strftime('%Y-%m-%d %H:%M:%S')
                )
            local_session.add(hourly_coin_rec)
    local_session.commit()
    local_session.close()


#===============================================================

def cc_sync_daily_coin_history_thread(symbol_list):

    # As MySQL Community Edition doesn't support multithreading
    # we need to create a local db session for each thread
    local_session = local_db_session_for_multithreading_calls()

    symbol = symbol_list[0]
    print "Daily: " + symbol

    # Find the newest record from the CryptoCompare_1hour_Chart for a Symbol
    chart_table_rec_max_date = local_session.query(func.max(CryptoCompare_Daily_History.data_date)) \
        .filter(CryptoCompare_Daily_History.symbol == symbol) \
        .one()

    # If there is data in chart_table_rec_max_date
    if chart_table_rec_max_date[0] is not None:

        # Calculate the Minutes
        time_difference = datetime.now().date() - (chart_table_rec_max_date[0]).date()
        day_difference = time_difference.days

        # Exit the block if the data is up to date
        if day_difference < 1:
            print "Daily Data up to date"
            local_session.close()
            return

        # Specify the limit as the time difference (Days) between last record and current time
        price_list_per_day = get_daily_price_history(symbol, 'USD', all_data=False, limit=day_difference)

        print "Calling Daily API with limit: " + str(day_difference)

    else:
        # Add All the Records if the DB Table is empty
        price_list_per_day = get_daily_price_history(symbol, 'USD', all_data=True)

        print "adding all Daily records to table: " + symbol

    for day_price in price_list_per_day:

        # Add data to the table is the Table is empty for a given Symbol or the record date is
        # greater than the max date in the Table for a given Symbol
        if (chart_table_rec_max_date[0] is None) or \
                (datetime.fromtimestamp(int(day_price['time'])) > chart_table_rec_max_date[0]):

            #print "Adding Data for: " + symbol

            daily_coin_rec = CryptoCompare_Daily_History(
                    symbol=symbol,
                    name=symbol,
                    open_usd=day_price['open'],
                    high_usd=day_price['high'],
                    low_usd=day_price['low'],
                    close_usd=day_price['close'],
                    volume_from=day_price['volumefrom'],
                    volume_to=day_price['volumeto'],
                    data_date=datetime.fromtimestamp(int(day_price['time'])).strftime('%Y-%m-%d %H:%M:%S')
                )
            local_session.add(daily_coin_rec)
    local_session.commit()
    local_session.close()
#===============================================================








#===============================================================
#=====  FILL CHART DATA TABLES  ================================
#===============================================================

# Time in minutes
DATA_INTERVAL_1HOUR_CHART = 1
DATA_INTERVAL_24HOUR_CHART = 2
DATA_INTERVAL_1WEEK_CHART = 5
DATA_INTERVAL_1MONTH_CHART = 10
DATA_INTERVAL_6MONTH_CHART = 10

#===============================================================

def update_cryptocompare_1hour_chart_data():
    update_cryptocompare_minute_chart_data(CryptoCompare_1hour_Chart, DATA_INTERVAL_1HOUR_CHART)
    clear_stale_chart_data(CryptoCompare_1hour_Chart, total_hours=1, total_minutes=0)


def update_cryptocompare_24hour_chart_data():
    update_cryptocompare_minute_chart_data(CryptoCompare_24hour_Chart, DATA_INTERVAL_24HOUR_CHART)
    clear_stale_chart_data(CryptoCompare_24hour_Chart, total_hours=24, total_minutes=0)

def update_cryptocompare_1week_chart_data():
    update_cryptocompare_minute_chart_data(CryptoCompare_1week_Chart, DATA_INTERVAL_1WEEK_CHART)
    clear_stale_chart_data(CryptoCompare_1week_Chart, total_hours=168, total_minutes=0)

def update_cryptocompare_1month_chart_data():
    update_cryptocompare_minute_chart_data(CryptoCompare_1month_Chart, DATA_INTERVAL_1MONTH_CHART)
    clear_stale_chart_data(CryptoCompare_1month_Chart, total_hours=720, total_minutes=0)

def update_cryptocompare_6month_chart_data():
    update_cryptocompare_minute_chart_data(CryptoCompare_6month_Chart, DATA_INTERVAL_6MONTH_CHART)
    clear_stale_chart_data(CryptoCompare_6month_Chart, total_hours=4320, total_minutes=0)

#===============================================================


def update_cryptocompare_minute_chart_data(db_class_name, gap_minutes):

    # As MySQL Community Edition doesn't support multithreading
    # we need to create a local db session for each thread
    local_session = local_db_session_for_multithreading_calls()

    coin_symbols = local_session.query(Coin_Master) \
        .with_entities(Coin_Master.symbol) \
        .all()

    # Repeat for all the Coin Symbols
    for coin_symbol in coin_symbols:
        symbol = coin_symbol[0]

        print symbol
        print

        # Find the newest record from the CryptoCompare_1hour_Chart for a Symbol
        chart_table_rec_max_date = local_session.query(func.max(db_class_name.data_date)) \
            .filter(db_class_name.symbol == symbol) \
            .one()


        # If there is No data in chart_table_rec_max_date (No records in Table?)
        if chart_table_rec_max_date[0] is None:
            # Fetch all Records from CryptoCompare_Minute_History for a Symbol
            cryptocompare_minute_data = local_session.query(CryptoCompare_Minute_History) \
                .filter(CryptoCompare_Minute_History.symbol == symbol) \
                .all()

            # Set the new_timestamp_for_chart_data to the minimum date of CryptoCompare_Minute_History for a coin
            chart_table_rec_max_date = local_session.query(func.min(CryptoCompare_Minute_History.data_date)) \
                .filter(CryptoCompare_Minute_History.symbol == symbol) \
                .one()

            new_timestamp_for_chart_data = chart_table_rec_max_date[0]

        # If chart_table_rec_max_date has a Date (Table has Records)
        else:

            # Create a new Timestamp with required minute gap
            new_timestamp_for_chart_data = chart_table_rec_max_date[0] + timedelta(minutes=gap_minutes)

            # Fetch All Records where Date is greater than the new_timestamp_for_chart_data for a Symbol
            cryptocompare_minute_data = local_session.query(CryptoCompare_Minute_History) \
                .filter(CryptoCompare_Minute_History.symbol == symbol) \
                .filter(CryptoCompare_Minute_History.data_date > new_timestamp_for_chart_data) \
                .all()

        # If cryptocompare_minute_data is not Null (No Records fulfilling the conditions)
        if not cryptocompare_minute_data is None:
            # Repeat for each Record in cryptocompare_minute_data
            for minute_data in cryptocompare_minute_data:

                # If current record date is greather than or equal to new_timestamp_for_chart_data
                if minute_data.data_date >= new_timestamp_for_chart_data:
                    # Add Record
                    tbl_record = db_class_name(symbol=symbol,
                                            data_date=minute_data.data_date,
                                            rate_usd=minute_data.low_usd
                                            )
                    local_session.add(tbl_record)

                    # Increment the timestamp value
                    new_timestamp_for_chart_data = new_timestamp_for_chart_data + timedelta(minutes=gap_minutes)
            local_session.commit()
    local_session.close()

#===============================================================


def clear_stale_chart_data(db_class_name, total_hours=0, total_minutes=0):

    # As MySQL Community Edition doesn't support multithreading
    # we need to create a local db session for each thread
    local_session = local_db_session_for_multithreading_calls()

    coin_symbols = session.query(Coin_Master) \
        .with_entities(Coin_Master.symbol) \
        .all()

    # Repeat for all the Coin Symbols
    for coin_symbol in coin_symbols:
        symbol = coin_symbol[0]

        print symbol
        print

        # Find the newest record from the CryptoCompare_1hour_Chart for a Symbol
        chart_table_rec_max_date = local_session.query(func.max(db_class_name.data_date)) \
            .filter(db_class_name.symbol == symbol) \
            .one()

        # If there is data in chart_table_rec_max_date
        if chart_table_rec_max_date[0] is not None:
            # Get the previous date based on the total data permitted in the table
            new_timestamp_for_chart_data = chart_table_rec_max_date[0] - timedelta(hours=total_hours, minutes=total_minutes)
            # Delete all the records older than the calculated date
            local_session.query(db_class_name) \
                .filter(db_class_name.symbol == symbol) \
                .filter(db_class_name.data_date < new_timestamp_for_chart_data) \
                .delete()
            local_session.commit()
    local_session.close()


#===============================================================