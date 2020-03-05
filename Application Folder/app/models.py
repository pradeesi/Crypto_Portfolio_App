# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager




#==========================================================
#===== GENERIC FUNCTIONS - START ============
#==========================================================



#==========================================================
#===== GENERIC FUNCTIONS - START ============
#==========================================================




#==========================================================
#===== AUTH MODEL - START ============
#==========================================================

class User(UserMixin, db.Model):
    """
    Create an User table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)
    portfolio_items = db.relationship('Portfolio_Manager', backref='user',
                                lazy='dynamic')

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.email)



# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    users = db.relationship('User', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)

#==========================================================
#===== AUTH MODEL - END ============
#==========================================================




#==========================================================
#===== PORTFOLIO MODEL - START ============
#==========================================================


class Portfolio_Manager(db.Model):
    """
    Create a Portfolio table
    """

    __tablename__ = 'portfolio_items'


    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    folio_id = db.Column(db.Integer, default=1)  #For future use (Multi-tenancy)
    item_id = db.Column(db.Integer, index=True, primary_key=True)
    coin_symbol = db.Column(db.String(30), db.ForeignKey('coin_master.symbol'))
    quantity = db.Column(db.Float)
    purchase_price = db.Column(db.Float)
    purchase_fees = db.Column(db.Float)
    broker = db.Column(db.String(150))
    purchase_date = db.Column(db.DateTime)
    is_available = db.Column(db.Boolean, default=True)
    sold_at_price = db.Column(db.Float)
    sold_fees = db.Column(db.Float)
    sold_on_date = db.Column(db.DateTime)
    remarks = db.Column(db.String(700))


    def __repr__(self):
        return '<Qty: {}>'.format(self.quantity)


#==========================================================
#===== PORTFOLIO MODEL - END ============
#==========================================================





#==========================================================
#===== COIN MODEL - START ============
#==========================================================

class Coin_Master(db.Model):
    """
    Create Coin master table
    """

    __tablename__ = 'coin_master'

    symbol = db.Column(db.String(30), index=True, primary_key=True)
    name =  db.Column(db.String(120), index=True)
    details = db.Column(db.String(512))
    icon_url = db.Column(db.String(256))
    portfolio_items = db.relationship('Portfolio_Manager', backref='coin_master',
                                lazy='dynamic')


    def __repr__(self):
        return '<Coin: {}>'.format(self.symbol)





#==========================================================
#===== COIN MODEL - END ============
#==========================================================



class Coin_Current_Data(db.Model):

    __tablename__ = 'coin_current_data'

    symbol = db.Column(db.String(30), index=True, primary_key=True)
    name = db.Column(db.String(120), index=True)
    coin_rank = db.Column(db.Integer)
    price_usd = db.Column(db.Float)
    price_btc = db.Column(db.Float)
    volume_usd_24h = db.Column(db.Float)
    market_cap_usd = db.Column(db.Float)
    available_supply = db.Column(db.Float)
    total_supply = db.Column(db.Float)
    max_supply = db.Column(db.Float)
    percentage_change_1h = db.Column(db.Float)
    percentage_change_24h = db.Column(db.Float)
    percentage_change_7d = db.Column(db.Float)
    last_updated = db.Column(db.DateTime)

    def __repr__(self):
        return '<Qty: {}>'.format(self.quantity)



class Coin_Daily_Data(db.Model):

    __tablename__ = 'coin_daily_data'

    rec_id = db.Column(db.Integer, index=True, primary_key=True)
    symbol = db.Column(db.String(30), index=True)
    name = db.Column(db.String(120), index=True)
    coin_rank = db.Column(db.Integer)
    price_usd = db.Column(db.Float)
    price_btc = db.Column(db.Float)
    volume_usd_24h = db.Column(db.Float)
    market_cap_usd = db.Column(db.Float)
    available_supply = db.Column(db.Float)
    total_supply = db.Column(db.Float)
    max_supply = db.Column(db.Float)
    percentage_change_1h = db.Column(db.Float)
    percentage_change_24h = db.Column(db.Float)
    percentage_change_7d = db.Column(db.Float)
    update_date_time = db.Column(db.DateTime, index=True)

    def __repr__(self):
        return '<Qty: {}>'.format(self.quantity)


class Coin_Weekly_Data(db.Model):

    __tablename__ = 'coin_weekly_data'

    rec_id = db.Column(db.Integer, index=True, primary_key=True)
    symbol = db.Column(db.String(30), index=True)
    name = db.Column(db.String(120), index=True)
    coin_rank = db.Column(db.Integer)
    price_usd = db.Column(db.Float)
    price_btc = db.Column(db.Float)
    volume_usd_24h = db.Column(db.Float)
    market_cap_usd = db.Column(db.Float)
    available_supply = db.Column(db.Float)
    total_supply = db.Column(db.Float)
    max_supply = db.Column(db.Float)
    percentage_change_1h = db.Column(db.Float)
    percentage_change_24h = db.Column(db.Float)
    percentage_change_7d = db.Column(db.Float)
    update_date_time = db.Column(db.DateTime, index=True)

    def __repr__(self):
        return '<Qty: {}>'.format(self.quantity)


class Coin_Monthly_Data(db.Model):

    __tablename__ = 'coin_monthly_data'

    rec_id = db.Column(db.Integer, index=True, primary_key=True)
    symbol = db.Column(db.String(30), index=True)
    name = db.Column(db.String(120), index=True)
    coin_rank = db.Column(db.Integer)
    price_usd = db.Column(db.Float)
    price_btc = db.Column(db.Float)
    volume_usd_24h = db.Column(db.Float)
    market_cap_usd = db.Column(db.Float)
    available_supply = db.Column(db.Float)
    total_supply = db.Column(db.Float)
    max_supply = db.Column(db.Float)
    percentage_change_1h = db.Column(db.Float)
    percentage_change_24h = db.Column(db.Float)
    percentage_change_7d = db.Column(db.Float)
    update_date_time = db.Column(db.DateTime, index=True)

    def __repr__(self):
        return '<Qty: {}>'.format(self.quantity)


class Coin_History(db.Model):
    """
    Full Coin History
    """

    __tablename__ = 'coin_historical_data'

    rec_id = db.Column(db.Integer, index=True, primary_key=True)
    symbol = db.Column(db.String(30), index=True)
    name = db.Column(db.String(120), index=True)
    data_date = db.Column(db.DateTime, index=True)
    open_usd = db.Column(db.Float)
    high_usd = db.Column(db.Float)
    low_usd = db.Column(db.Float)
    close_usd = db.Column(db.Float)


    def __repr__(self):
        return '<Coin: {}>'.format(self.symbol)


class CryptoCompare_Minute_History(db.Model):
    """
    Coin History Per Minute
    """

    __tablename__ = 'cryptocompare_minute_history'

    rec_id = db.Column(db.Integer, index=True, primary_key=True)
    symbol = db.Column(db.String(30), index=True)
    name = db.Column(db.String(120), index=True)
    data_date = db.Column(db.DateTime, index=True)
    open_usd = db.Column(db.Float)
    high_usd = db.Column(db.Float)
    low_usd = db.Column(db.Float)
    close_usd = db.Column(db.Float)
    volume_from = db.Column(db.Float)
    volume_to = db.Column(db.Float)


class CryptoCompare_Hourly_History(db.Model):
    """
    Coin History Per Hour
    """

    __tablename__ = 'cryptocompare_hourly_history'

    rec_id = db.Column(db.Integer, index=True, primary_key=True)
    symbol = db.Column(db.String(30), index=True)
    name = db.Column(db.String(120), index=True)
    data_date = db.Column(db.DateTime, index=True)
    open_usd = db.Column(db.Float)
    high_usd = db.Column(db.Float)
    low_usd = db.Column(db.Float)
    close_usd = db.Column(db.Float)
    volume_from = db.Column(db.Float)
    volume_to = db.Column(db.Float)
    

class CryptoCompare_Daily_History(db.Model):
    """
    Coin History Per Day
    """

    __tablename__ = 'cryptocompare_daily_history'

    rec_id = db.Column(db.Integer, index=True, primary_key=True)
    symbol = db.Column(db.String(30), index=True)
    name = db.Column(db.String(120), index=True)
    data_date = db.Column(db.DateTime, index=True)
    open_usd = db.Column(db.Float)
    high_usd = db.Column(db.Float)
    low_usd = db.Column(db.Float)
    close_usd = db.Column(db.Float)
    volume_from = db.Column(db.Float)
    volume_to = db.Column(db.Float)




class CryptoCompare_1hour_Chart(db.Model):

    __tablename__ = 'cryptocompare_1hour_chart'

    rec_id = db.Column(db.Integer, index=True, primary_key=True)
    symbol = db.Column(db.String(30), index=True)
    data_date = db.Column(db.DateTime, index=True)
    rate_usd = db.Column(db.Float)


class CryptoCompare_24hour_Chart(db.Model):

    __tablename__ = 'cryptocompare_24hour_chart'

    rec_id = db.Column(db.Integer, index=True, primary_key=True)
    symbol = db.Column(db.String(30), index=True)
    data_date = db.Column(db.DateTime, index=True)
    rate_usd = db.Column(db.Float)


class CryptoCompare_1week_Chart(db.Model):

    __tablename__ = 'cryptocompare_1week_chart'

    rec_id = db.Column(db.Integer, index=True, primary_key=True)
    symbol = db.Column(db.String(30), index=True)
    data_date = db.Column(db.DateTime, index=True)
    rate_usd = db.Column(db.Float)


class CryptoCompare_1month_Chart(db.Model):

    __tablename__ = 'cryptocompare_1month_chart'

    rec_id = db.Column(db.Integer, index=True, primary_key=True)
    symbol = db.Column(db.String(30), index=True)
    data_date = db.Column(db.DateTime, index=True)
    rate_usd = db.Column(db.Float)


class CryptoCompare_6month_Chart(db.Model):

    __tablename__ = 'cryptocompare_6month_chart'

    rec_id = db.Column(db.Integer, index=True, primary_key=True)
    symbol = db.Column(db.String(30), index=True)
    data_date = db.Column(db.DateTime, index=True)
    rate_usd = db.Column(db.Float)


class CryptoCompare_Nyear_Chart(db.Model):


    __tablename__ = 'cryptocompare_nyear_chart'

    rec_id = db.Column(db.Integer, index=True, primary_key=True)
    symbol = db.Column(db.String(30), index=True)
    data_date = db.Column(db.DateTime, index=True)
    rate_usd = db.Column(db.Float)

