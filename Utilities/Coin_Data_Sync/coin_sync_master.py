import multiprocessing

from cryptocompare.cryptocompare_db_sync import cc_sync_minute_coin_history, cc_sync_hourly_coin_history, \
                        cc_sync_daily_coin_history, update_cryptocompare_1hour_chart_data, update_cryptocompare_24hour_chart_data, \
                        update_cryptocompare_1week_chart_data, update_cryptocompare_6month_chart_data


from coinmarketcap.coinmarketcap_db_sync import cmc_update_coin_master, cmc_sync_db_with_coin_data


import time

while True:



    #==========================================================
    #==== Coinmarketcap Data Sync
    #==========================================================
    # Update Coin Master Table with List of Coins
    cmc_update_coin_master()

    # Update Coin Current Data
    cmc_sync_db_with_coin_data()
    #==========================================================




    #==========================================================
    #===== Cryptocompare Data Sync
    #==========================================================

    NO_OF_WORKER_THREADS = 10

    # Update minute coin history
    cc_sync_minute_coin_history(NO_OF_WORKER_THREADS)

    # Update hourly coin history
    cc_sync_hourly_coin_history(NO_OF_WORKER_THREADS)

    # Update daily coin history
    cc_sync_daily_coin_history(NO_OF_WORKER_THREADS)


    # Update cryptocompare chart data

    proc_1hour_chart_data = multiprocessing.Process(target=update_cryptocompare_1hour_chart_data)
    proc_1hour_chart_data.start()

    proc_24hour_chart_data = multiprocessing.Process(target=update_cryptocompare_24hour_chart_data)
    proc_24hour_chart_data.start()

    proc_1week_chart_data = multiprocessing.Process(target=update_cryptocompare_1week_chart_data)
    proc_1week_chart_data.start()

    proc_6month_chart_data = multiprocessing.Process(target=update_cryptocompare_6month_chart_data)
    proc_6month_chart_data.start()

    proc_1hour_chart_data.join()
    proc_24hour_chart_data.join()
    proc_1week_chart_data.join()
    proc_6month_chart_data.join()

    #==========================================================

    time.sleep(60)
