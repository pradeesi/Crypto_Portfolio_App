# app/util_scripts/api_task_scheduler.py




from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit

from datetime import datetime


def schedule_api_tasks(app):
	try:
		#scheduler = BackgroundScheduler()
		#scheduler.start()

		#sync_historical_data(app)
		#sync_historical_data_per_minute(app)
		pass

		#scheduler.add_job(
		#	func=price_sync_from_cryptocompare,
		#	args=[app],
		#	trigger=IntervalTrigger(seconds=60),
		#	id='cryptocompare_coin_sync_current_data',
		#	name='Pull Coin Data from CryptoCompare after every 5 seconds',
		#	replace_existing=True)


		#scheduler.add_job(
		#	func=sync_db_with_coin_data,
		#	args=[app],
		#	trigger=IntervalTrigger(minutes=5.5),
		#	id='coinmarketcap_coin_sync_current_data',
		#	name='Pull Coin Data from coinmarketcap after every 6 Minutes',
		#	replace_existing=True)


		#scheduler.add_job(
		#	func=sync_coin_daily_data,
		#	args=[app],
		#	trigger=IntervalTrigger(minutes=6),
		#	id='coinmarketcap_coin_sync_daily_data',
		#	name='Update Daily Coin Data table with current coin data after every 10 minutes',
		#	replace_existing=True)


		#scheduler.add_job(
		#	func=sync_coin_weekly_data,
		#	args=[app],
		#	trigger=IntervalTrigger(minutes=12),
		#	id='coinmarketcap_coin_sync_weekly_data',
		#	name='Update Monthly Coin Data table with current coin data after every 20 minutes',
		#	replace_existing=True)


		#scheduler.add_job(
		#	func=sync_coin_monthly_data,
		#	args=[app],
		#	trigger=IntervalTrigger(minutes=20),
		#	id='coinmarketcap_coin_sync_monthly_data',
		#	name='Update Monthly Coin Data table with current coin data after every 30 minutes',
		#	replace_existing=True)

		# Shut down the scheduler when exiting the app
		#atexit.register(lambda: scheduler.shutdown())
	except:
		#scheduler.shutdown()
		pass


