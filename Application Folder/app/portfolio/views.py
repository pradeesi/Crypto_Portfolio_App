# app/portfolio/views.py

from flask import flash, redirect, render_template, url_for, request, abort
from flask_login import login_required, current_user
import json
#import datetime
from sqlalchemy import and_, or_, not_, func, cast, DATE
from . import portfolio
from forms import Add_Portfolio_Item_Form
from .. import db
from ..models import CryptoCompare_Nyear_Chart, CryptoCompare_1month_Chart, CryptoCompare_6month_Chart, CryptoCompare_1week_Chart, CryptoCompare_24hour_Chart, Portfolio_Manager, Coin_Master, Coin_Current_Data, Coin_Daily_Data, Coin_Weekly_Data, Coin_History

from ..util_scripts.custom_date_time_functions import get_past_date




#==========================================================
#======== Live Price ===========
#==========================================================
@portfolio.route('/portfolio/live_price/<int:id>/<string:symbol>/<string:name>', methods=['GET'])
@login_required
def get_live_price(id,symbol,name):

    return render_template('portfolio/portfolio_item_live_price.html',folio_item_id=id, folio_item_symbol=symbol, folio_item_name=name, title='Live Price')



#==========================================================
#======== Portfolio Dashbaord ===========
#==========================================================
@portfolio.route('/portfolio/portfolio_dashbaord', methods=['GET'])
@login_required
def portfolio_dashbaord():

    # Total Coins, Current Price and Current Asset Value
    query = Portfolio_Manager.query \
        .join(Coin_Master) \
        .with_entities(Coin_Master.name, Coin_Master.symbol, func.sum(Portfolio_Manager.quantity).label('total')) \
        .filter(Portfolio_Manager.user_id == current_user.id) \
        .group_by(Coin_Master.symbol) \
        .order_by(Coin_Master.symbol)

    coin_total_rec = query.all()

    coin_total_labels = []
    coin_total_values = []
    coin_total_assets_value = []

    current_price_values = []
    current_price_labels = []


    if len(coin_total_rec) > 0:
        for row in coin_total_rec:
            temp_dict = dict(zip(row.keys(), row))
            coin_total_labels.append((temp_dict['name'] + ' (' + temp_dict['symbol'] + ')'))
            coin_total_values.append(temp_dict['total'])
            current_price = ((Coin_Current_Data.query.with_entities(Coin_Current_Data.price_usd).filter(
                Coin_Current_Data.symbol == temp_dict['symbol']).one())[0])
            coin_total_assets_value.append((temp_dict['total'] * current_price))
            current_price_values.append(current_price)
            current_price_labels.append(temp_dict['symbol'])



    # INVESTED AMOUNT
    query = Portfolio_Manager.query \
        .join(Coin_Master) \
        .with_entities(Coin_Master.name, Coin_Master.symbol, Portfolio_Manager.quantity, Portfolio_Manager.purchase_price) \
        .filter(Portfolio_Manager.user_id == current_user.id) \
        .order_by(Coin_Master.symbol)

    coin_rec = query.all()

    coin_purchase_value_dict = {}
    invested_amount_labels = []
    invested_amount_values = []

    if len(coin_rec) > 0:
        for row in coin_rec:
            temp_dict = dict(zip(row.keys(), row))
            temp_key = (temp_dict['name'] + ' (' + temp_dict['symbol'] + ')')
            coin_purchase_value_dict[temp_key] = (coin_purchase_value_dict[temp_key] if temp_key in coin_purchase_value_dict else 0) + (temp_dict['quantity'] * temp_dict['purchase_price'])


        invested_amount_labels = coin_purchase_value_dict.keys()
        invested_amount_values = coin_purchase_value_dict.values()




    return render_template('portfolio/portfolio_items_dashboard.html',coin_total_values=coin_total_values, coin_total_labels=coin_total_labels, coin_total_assets_value=coin_total_assets_value, \
                           invested_amount_labels=invested_amount_labels, invested_amount_values=invested_amount_values, current_price_values=current_price_values, current_price_labels=current_price_labels, title='Dashbaord')



#==========================================================
#======== Add Portfolio Item ===========
#==========================================================
@portfolio.route('/portfolio/add', methods=['GET', 'POST'])
@login_required
def add_portfolio_item():
    """
    Handle requests to the /portfolio/add route
    Add a new Portfolio Item to the database through the Add Portfolio Item form
    """

    form = Add_Portfolio_Item_Form()
    
    # Populate Coin List
    #coins = Coin_Master.query.with_entities(Coin_Master.coin_id, Coin_Master.name, Coin_Master.symbol).order_by(Coin_Master.name).all()
    #coin_list = []
    #for coin in coins:
    #    coin_touple = (coin.coin_id, coin.symbol+ " - " +coin.name)
    #    coin_list.append(coin_touple)
    #form.coin.choices = coin_list

    form.coin.choices = [(coin.symbol, coin.symbol+ " - " +coin.name) for coin in (Coin_Master.query.with_entities(Coin_Master.name, Coin_Master.symbol).order_by(Coin_Master.symbol).all())]


    if request.method == 'POST' and form.validate_on_submit():

        portfolio_item = Portfolio_Manager(user_id=current_user.id,
                        folio_id=1,
                        coin_symbol=form.coin.data,
                        quantity=form.quantity.data,
                        purchase_price=form.purchase_price.data,
                        purchase_fees=form.purchase_fees.data,
                        purchase_date=form.purchase_date.data,
                        is_available=True,
                        broker=form.broker.data,
                        remarks=form.remarks.data)

        # add portfolio item to the database
        db.session.add(portfolio_item)
        db.session.commit()
        flash('Portfolio item successfully added.')

        # redirect to the login page
        return redirect(url_for('portfolio.add_portfolio_item'))

    # add portfolio item template
    return render_template('portfolio/add_portfolio_item.html', form=form, title='Add Portfolio Item')
#==========================================================




# ==========================================================
# ======== Update Portfolio Item ===========
# ==========================================================
@portfolio.route('/portfolio/update_item/<int:id>', methods=['GET', 'POST'])
@login_required
def update_portfolio_items(id):
    """
    Update the Portfolio Item for the logged in user.
    """

    form = Add_Portfolio_Item_Form()

    query = Portfolio_Manager.query.filter(and_(Portfolio_Manager.item_id == id, \
                                                Portfolio_Manager.user_id == current_user.id))

    # Fetch Record
    portfolio_item_rec = query.first()

    # abort operation if this record doesn't belong to logged-in user
    if portfolio_item_rec == None:
        abort(403)

    form.coin.choices = [(coin.symbol, coin.symbol + " - " + coin.name) for coin in (
        Coin_Master.query.with_entities(Coin_Master.name, Coin_Master.symbol).order_by(Coin_Master.symbol).all())]


    # If it's a GET request
    if request.method == 'GET':

        form.coin.data = portfolio_item_rec.coin_symbol
        form.quantity.data = portfolio_item_rec.quantity
        form.purchase_price.data = portfolio_item_rec.purchase_price
        form.purchase_fees.data = portfolio_item_rec.purchase_fees
        form.purchase_date.data = portfolio_item_rec.purchase_date
        form.broker.data = portfolio_item_rec.broker
        form.remarks.data = portfolio_item_rec.remarks
        form.submit.label.text = "Update"

    # If its a POST request
    if request.method == 'POST' and form.validate_on_submit():

        portfolio_item_rec.coin_symbol = form.coin.data
        portfolio_item_rec.coin_symbol = form.coin.data
        portfolio_item_rec.quantity = form.quantity.data
        portfolio_item_rec.purchase_price = form.purchase_price.data
        portfolio_item_rec.purchase_fees = form.purchase_fees.data
        portfolio_item_rec.purchase_date = form.purchase_date.data
        portfolio_item_rec.broker = form.broker.data
        portfolio_item_rec.remarks = form.remarks.data

        # update portfolio item
        db.session.commit()
        flash('Portfolio item updated successfully.')

        # redirect to the portfolio item details
        return redirect(url_for('portfolio.portfolio_item_details', id=id))

    # update portfolio item template
    return render_template('portfolio/update_portfolio_item.html', form=form, item_id=id, title='Update Portfolio Item')


# ==========================================================



#==========================================================
#======== Delete Portfolio Item ===========
#==========================================================
@portfolio.route('/portfolio/del_item/<int:id>', methods=['GET'])
@login_required
def del_portfolio_items(id):
    """
    Delete the Portfolio Item for the logged in user.
    """

    query = Portfolio_Manager.query.filter(and_(Portfolio_Manager.item_id==id, \
            Portfolio_Manager.user_id == current_user.id))

    
    # abort operation if this record doesn't belong to logged-in user
    if len(query.all()) <= 0:
        abort(403)
    else:
    # delete the recored
        query.delete()
        db.session.commit()
        
    return redirect(url_for('portfolio.list_portfolio_items'))
#==========================================================






#==========================================================
#======== Show Portfolio Item Details ===========
#==========================================================

@portfolio.route('/portfolio/item/<int:id>', methods=['GET'])
@login_required
def portfolio_item_details(id):
    
    # Get folio item data
    folio_item = Portfolio_Manager.query \
            .join(Coin_Master) \
            .with_entities(Coin_Master.name, \
                Coin_Master.symbol, \
                Portfolio_Manager.item_id, \
                Portfolio_Manager.quantity, \
                Portfolio_Manager.purchase_price, \
                Portfolio_Manager.purchase_fees, \
                Portfolio_Manager.purchase_date, \
                Portfolio_Manager.broker, \
                Portfolio_Manager.remarks) \
            .filter(and_(Portfolio_Manager.item_id==id, Portfolio_Manager.user_id == current_user.id)) \
            .one()

    folio_item_dict =  dict(zip(folio_item.keys(), folio_item))

    if len(folio_item_dict) <= 0:
        abort(404)


    # Get Coin Data
    coin_data = Coin_Current_Data.query \
            .filter(Coin_Current_Data.symbol == folio_item.symbol) \
            .one()

    coin_data_dict = coin_data.__dict__


    # Prepare Chart Data
    chart_data_24h = (Coin_Daily_Data.query
                    .with_entities(CryptoCompare_24hour_Chart.data_date,
                        CryptoCompare_24hour_Chart.rate_usd)
                    .filter(CryptoCompare_24hour_Chart.symbol == folio_item.symbol)
                    .all()
                    )


    chart_data_24h_labels = []
    chart_data_24h_values = []
    for row in chart_data_24h:
        chart_data_24h_labels.append((row.data_date).strftime('%H:%M'))
        chart_data_24h_values.append(row.rate_usd)


    # Prepare Chart Data
    chart_data_7d = (CryptoCompare_1week_Chart.query
                    .with_entities(CryptoCompare_1week_Chart.data_date,
                                CryptoCompare_1week_Chart.rate_usd)
                    .filter(CryptoCompare_1week_Chart.symbol == folio_item.symbol)
                    .all()
                    )


    chart_data_7d_labels = []
    chart_data_7d_values = []
    for row in chart_data_7d:
        chart_data_7d_labels.append((row.data_date).strftime('%m-%d'))
        chart_data_7d_values.append(row.rate_usd)




    # This step is required to convert long number (Prices in Billion) to readable String
    # To avoid scientific notation / exponential notation
    coin_data_dict['market_cap_usd'] = '{:20,.0f}'.format(coin_data_dict['market_cap_usd'])
    coin_data_dict['volume_usd_24h'] = '{:20,.0f}'.format(coin_data_dict['volume_usd_24h'])
    if coin_data_dict['price_btc'] < 1:
        coin_data_dict['price_btc'] = '{:.8f}'.format(coin_data_dict['price_btc'])
    if coin_data_dict['max_supply'] != None:
        coin_data_dict['max_supply'] = '{:20,.0f}'.format(coin_data_dict['max_supply'])

    
    # Calcuations
    folio_item_dict['current_price'] = (Coin_Current_Data.query.with_entities(Coin_Current_Data.price_usd).filter(Coin_Current_Data.symbol == folio_item_dict['symbol']).one())[0]
    folio_item_dict['original_asset_value'] = (float("{0:.2f}".format(folio_item_dict['quantity'] * folio_item_dict['purchase_price'])))
    folio_item_dict['current_asset_value'] = float("{0:.2f}".format(folio_item_dict['quantity'] * folio_item_dict['current_price']))
    folio_item_dict['profit_loss_amt'] = float("{0:.2f}".format(folio_item_dict['current_asset_value'] - folio_item_dict['original_asset_value']))
    if folio_item_dict['current_price'] > folio_item_dict['purchase_price']:
        folio_item_dict['change_percentage'] = float("{0:.2f}".format(((folio_item_dict['current_price'] - folio_item_dict['purchase_price']) / folio_item_dict['purchase_price']) * 100))
        folio_item_dict['css_class'] = 'success'
    else:
        folio_item_dict['change_percentage'] = -1 * float("{0:.2f}".format(((folio_item_dict['purchase_price'] - folio_item_dict['current_price']) / folio_item_dict['current_price']) * 100))
        folio_item_dict['css_class'] = 'danger'


    


    return render_template('portfolio/portfolio_item_details.html',
                           folio_item=folio_item_dict, coin_data=coin_data_dict, chart_data_24h_labels=chart_data_24h_labels, chart_data_24h_values=chart_data_24h_values, chart_data_7d_labels=chart_data_7d_labels, chart_data_7d_values=chart_data_7d_values, title="Portfolio Item Details")

#==========================================================






#==========================================================
#======== List Portfolio Item ===========
#==========================================================
@portfolio.route('/portfolio/list_items', methods=['GET'])
@login_required
def list_portfolio_items():
    """
    Handle requests to the /portfolio/add route
    Add a new Portfolio Item to the database through the Add Portfolio Item form
    """


    #from datetime import date
    #from dateutil.relativedelta import relativedelta
    #six_months = date.today() + relativedelta(months=+6)



    #sync_historical_data_per_minute()


    #from datetime import datetime, timedelta
    #futuredate = datetime.now() + timedelta(days=10)

    #query = Portfolio_Manager.query.filter(Portfolio_Manager.user_id == current_user.id).order_by(Portfolio_Manager.item_id)
        
    # FOR RESULTS WITH ALL FIELDS
    #result_list = [u.__dict__ for u in query.all()]
    #print result_list


    query = Portfolio_Manager.query \
            .join(Coin_Master) \
            .with_entities(Coin_Master.name, Coin_Master.symbol, Portfolio_Manager.item_id, Portfolio_Manager.quantity, Portfolio_Manager.purchase_price, Portfolio_Manager.purchase_fees,Portfolio_Manager.purchase_date,Portfolio_Manager.remarks) \
            .filter(Portfolio_Manager.user_id == current_user.id) \
            .order_by(Portfolio_Manager.item_id)

    # FOR RESULTS WITH SELECTED FIELDS
    folio_items = []
    for row in query.all():
        
        folio_dict = dict(zip(row.keys(), row))
        folio_dict['current_price'] = (Coin_Current_Data.query.with_entities(Coin_Current_Data.price_usd).filter(Coin_Current_Data.symbol == folio_dict['symbol']).one())[0]
        folio_dict['original_asset_value'] = (float("{0:.2f}".format(folio_dict['quantity'] * folio_dict['purchase_price'])))
        folio_dict['current_asset_value'] = (float("{0:.2f}".format(folio_dict['quantity'] * folio_dict['current_price'])))
        folio_dict['profit_loss_amt'] = (float("{0:.2f}".format(folio_dict['current_asset_value'] - folio_dict['original_asset_value']))) - folio_dict['purchase_fees']

        folio_dict['change_percentage'] = float("{0:.2f}".format(((folio_dict['current_asset_value'] - folio_dict[
            'original_asset_value']) / folio_dict['original_asset_value']) * 100))

        if folio_dict['current_price'] > folio_dict['purchase_price']:
            folio_dict['css_class'] = 'success'
        else:
            folio_dict['css_class'] = 'danger'
        
        folio_items.append(folio_dict)


        #print json.dumps(result_list)


    return render_template('portfolio/list_portfolio_items.html',
                           folio_items=folio_items, title="Portfolio Items")
#==========================================================





# ==========================================================
# ======== Show Portfolio Item Charts ===========
# ==========================================================

@portfolio.route('/portfolio/item_charts/<int:id>/<string:duration>', methods=['GET'])
@login_required
def portfolio_item_charts(id,duration):
    # Get folio item data
    folio_item = Portfolio_Manager.query \
        .join(Coin_Master) \
        .with_entities(Coin_Master.name, \
                       Coin_Master.symbol, \
                       Portfolio_Manager.item_id) \
        .filter(and_(Portfolio_Manager.item_id == id, Portfolio_Manager.user_id == current_user.id)) \
        .one()

    folio_item_dict = dict(zip(folio_item.keys(), folio_item))

    if len(folio_item_dict) <= 0:
        abort(404)


    chart_data = []
    chart_duration = ''
    chart_heading = ''



    # Prepare Chart Data
    if duration == '1D':

        chart_data = (Coin_Daily_Data.query
                          .with_entities(CryptoCompare_24hour_Chart.data_date,
                                         CryptoCompare_24hour_Chart.rate_usd)
                          .filter(CryptoCompare_24hour_Chart.symbol == folio_item.symbol)
                          .all()
                        )

        chart_heading = 'Data from last 24 hours'

    elif duration == '7D':

        chart_data = (CryptoCompare_1week_Chart.query
                         .with_entities(CryptoCompare_1week_Chart.data_date,
                                        CryptoCompare_1week_Chart.rate_usd)
                         .filter(CryptoCompare_1week_Chart.symbol == folio_item.symbol)
                         .all()
                         )

        chart_heading = 'Data from last 7 Days'

    elif duration == '1M':

        chart_data = (CryptoCompare_1month_Chart.query
                         .with_entities(CryptoCompare_1month_Chart.data_date,
                                        CryptoCompare_1month_Chart.rate_usd)
                         .filter(CryptoCompare_1month_Chart.symbol == folio_item.symbol)
                         .all()
                         )

        chart_heading = 'Data from last 1 Month'


    elif duration == '6M':

        chart_data = (CryptoCompare_6month_Chart.query
                         .with_entities(CryptoCompare_6month_Chart.data_date,
                                        CryptoCompare_6month_Chart.rate_usd)
                         .filter(CryptoCompare_6month_Chart.symbol == folio_item.symbol)
                         .all()
                         )

        chart_heading = 'Data from last 6 Months'

    elif duration == '1Y':

        chart_data = (CryptoCompare_Nyear_Chart.query
                         .with_entities(CryptoCompare_Nyear_Chart.data_date,
                                        CryptoCompare_Nyear_Chart.rate_usd)
                         .filter(CryptoCompare_Nyear_Chart.symbol == folio_item.symbol)
                         .all()
                         )

        chart_heading = 'Data from last 1 Year'


    elif duration == 'ATD':

        chart_data = (CryptoCompare_Nyear_Chart.query
                         .with_entities(CryptoCompare_Nyear_Chart.data_date,
                                        CryptoCompare_Nyear_Chart.rate_usd)
                         .filter(CryptoCompare_Nyear_Chart.symbol == folio_item.symbol)
                         .all()
                         )

        chart_heading = 'All Time Data'


    chart_data_labels = []
    chart_data_values = []
    for row in chart_data:
        chart_data_labels.append((row.data_date).strftime('%H:%M'))
        chart_data_values.append(row.rate_usd)

    return render_template('portfolio/portfolio_item_charts.html',
                           folio_item=folio_item_dict, chart_heading=chart_heading, chart_duration=duration,
                           chart_data_labels=chart_data_labels, chart_data_values=chart_data_values,
                           title="Portfolio Item Details")

# ==========================================================





# ==========================================================
# ======== GET Charts Data for a Portfolio Item ===========
# ==========================================================

@portfolio.route('/portfolio/item_chart_data/<int:id>', methods=['GET'])
@login_required
def portfolio_item_chart_data(id):
    # Get folio item data
    folio_item = Portfolio_Manager.query \
        .join(Coin_Master) \
        .with_entities(Coin_Master.name, \
                       Coin_Master.symbol, \
                       Portfolio_Manager.item_id) \
        .filter(and_(Portfolio_Manager.item_id == id, Portfolio_Manager.user_id == current_user.id)) \
        .one()

    folio_item_dict = dict(zip(folio_item.keys(), folio_item))

    if len(folio_item_dict) <= 0:
        abort(404)



    # Prepare Chart Data
    chart_data_24h = (Coin_Daily_Data.query
                      .with_entities(CryptoCompare_24hour_Chart.data_date,
                                     CryptoCompare_24hour_Chart.rate_usd)
                      .filter(CryptoCompare_24hour_Chart.symbol == folio_item.symbol)
                      .all()
                      )

    chart_data_24h_labels = []
    chart_data_24h_values = []
    for row in chart_data_24h:
        chart_data_24h_labels.append((row.data_date).strftime('%H:%M'))
        chart_data_24h_values.append(row.rate_usd)

    # Prepare Chart Data
    chart_data_7d = (CryptoCompare_1week_Chart.query
                     .with_entities(CryptoCompare_1week_Chart.data_date,
                                    CryptoCompare_1week_Chart.rate_usd)
                     .filter(CryptoCompare_1week_Chart.symbol == folio_item.symbol)
                     .all()
                     )

    chart_data_7d_labels = []
    chart_data_7d_values = []
    for row in chart_data_7d:
        chart_data_7d_labels.append((row.data_date).strftime('%m-%d'))
        chart_data_7d_values.append(row.rate_usd)




    return render_template('portfolio/portfolio_item_charts.html',
                           folio_item=folio_item_dict,
                           chart_data_24h_labels=chart_data_24h_labels, chart_data_24h_values=chart_data_24h_values,
                           chart_data_7d_labels=chart_data_7d_labels, chart_data_7d_values=chart_data_7d_values,
                           title="Portfolio Item Details")

# ==========================================================
