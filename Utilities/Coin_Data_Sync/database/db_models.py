from sqlalchemy import Column, Integer, String, DateTime, Float

from .db_init import Base



class Coin_Master(Base):
    """
    Create Coin master table
    """

    __tablename__ = 'coin_master'

    symbol = Column(String(30), index=True, primary_key=True)
    name =  Column(String(120), index=True)
    details = Column(String(512))
    icon_url = Column(String(256))


    def __repr__(self):
        return '<Coin: {}>'.format(self.symbol)



class Coin_Current_Data(Base):

    __tablename__ = 'coin_current_data'

    symbol = Column(String(30), index=True, primary_key=True)
    name = Column(String(120), index=True)
    coin_rank = Column(Integer)
    price_usd = Column(Float)
    price_btc = Column(Float)
    volume_usd_24h = Column(Float)
    market_cap_usd = Column(Float)
    available_supply = Column(Float)
    total_supply = Column(Float)
    max_supply = Column(Float)
    percentage_change_1h = Column(Float)
    percentage_change_24h = Column(Float)
    percentage_change_7d = Column(Float)
    last_updated = Column(DateTime)

    def __repr__(self):
        return '<Qty: {}>'.format(self.quantity)




class CryptoCompare_Minute_History(Base):
    """
    Coin History Per Minute
    """

    __tablename__ = 'cryptocompare_minute_history'

    rec_id = Column(Integer, index=True, primary_key=True)
    symbol = Column(String(30), index=True)
    name = Column(String(120), index=True)
    data_date = Column(DateTime, index=True)
    open_usd = Column(Float)
    high_usd = Column(Float)
    low_usd = Column(Float)
    close_usd = Column(Float)
    volume_from = Column(Float)
    volume_to = Column(Float)




class CryptoCompare_Hourly_History(Base):
    """
    Coin History Per Hour
    """

    __tablename__ = 'cryptocompare_hourly_history'

    rec_id = Column(Integer, index=True, primary_key=True)
    symbol = Column(String(30), index=True)
    name = Column(String(120), index=True)
    data_date = Column(DateTime, index=True)
    open_usd = Column(Float)
    high_usd = Column(Float)
    low_usd = Column(Float)
    close_usd = Column(Float)
    volume_from = Column(Float)
    volume_to = Column(Float)




class CryptoCompare_Daily_History(Base):
    """
    Coin History Per Day
    """

    __tablename__ = 'cryptocompare_daily_history'

    rec_id = Column(Integer, index=True, primary_key=True)
    symbol = Column(String(30), index=True)
    name = Column(String(120), index=True)
    data_date = Column(DateTime, index=True)
    open_usd = Column(Float)
    high_usd = Column(Float)
    low_usd = Column(Float)
    close_usd = Column(Float)
    volume_from = Column(Float)
    volume_to = Column(Float)



class CryptoCompare_1hour_Chart(Base):

    __tablename__ = 'cryptocompare_1hour_chart'

    rec_id = Column(Integer, primary_key=True)
    symbol = Column(String(10), index=True)
    data_date = Column(DateTime, index=True)
    rate_usd = Column(Float)


class CryptoCompare_24hour_Chart(Base):

    __tablename__ = 'cryptocompare_24hour_chart'

    rec_id = Column(Integer, primary_key=True)
    symbol = Column(String(10), index=True)
    data_date = Column(DateTime, index=True)
    rate_usd = Column(Float)


class CryptoCompare_1week_Chart(Base):

    __tablename__ = 'cryptocompare_1week_chart'

    rec_id = Column(Integer, primary_key=True)
    symbol = Column(String(10), index=True)
    data_date = Column(DateTime, index=True)
    rate_usd = Column(Float)


class CryptoCompare_1month_Chart(Base):

    __tablename__ = 'cryptocompare_1month_chart'

    rec_id = Column(Integer, primary_key=True)
    symbol = Column(String(10), index=True)
    data_date = Column(DateTime, index=True)
    rate_usd = Column(Float)


class CryptoCompare_6month_Chart(Base):

    __tablename__ = 'cryptocompare_6month_chart'

    rec_id = Column(Integer, primary_key=True)
    symbol = Column(String(10), index=True)
    data_date = Column(DateTime, index=True)
    rate_usd = Column(Float)


class CryptoCompare_Nyear_Chart(Base):


    __tablename__ = 'cryptocompare_nyear_chart'

    rec_id = Column(Integer, primary_key=True)
    symbol = Column(String(10), index=True)
    data_date = Column(DateTime, index=True)
    rate_usd = Column(Float)
