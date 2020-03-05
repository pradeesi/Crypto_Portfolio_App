# app/portfolio/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, DateTimeField, IntegerField, DecimalField, SelectField, SubmitField, TextAreaField, ValidationError
from wtforms.validators import DataRequired, EqualTo
from datetime import date

from ..models import Portfolio_Manager, User



class Add_Portfolio_Item_Form(FlaskForm):
    """
    Form to add a new Portfolio item
    """

    coin = SelectField('Coin:',validators=[DataRequired()])
    quantity = DecimalField('Quantity:',validators=[DataRequired()])
    purchase_price = DecimalField('Purchase Price:',validators=[DataRequired()])
    purchase_fees = DecimalField('Exchange Purchase Fees:',validators=[DataRequired()])
    purchase_date = DateTimeField('Purchase Date:',format="%Y-%m-%d", default=date.today(),validators=[DataRequired()])
    broker = StringField('Broker:')
    remarks = TextAreaField('Remarks:')
    submit = SubmitField('Add')



class Del_Portfolio_Item_Form(FlaskForm):
    """
    Form to Delete a Portfolio item
    """
    
    folio_id = IntegerField('FolioID:', validators=[DataRequired()])
    user_id = IntegerField('UserID:', validators=[DataRequired()])
    submit = SubmitField('Delete')

    def validate_portfolio_item(self, field):
        if not Portfolio_Manager.query.filter_by(item_id=field.data).first():
            raise ValidationError('Invalid Portfolio Item.')

    def validate_user(self, field):
        if User.query.filter_by(id=field.data).first():
            raise ValidationError('Portfolio Item does not belong to this user.')



class Close_Portfolio_Item_Form(FlaskForm):
    """
    Form to Close a Portfolio item
    """
    
    folio_id = IntegerField('FolioID:', validators=[DataRequired()])
    user_id = IntegerField('UserID:', validators=[DataRequired()])
    sold_at_price = DecimalField("Quantity:",validators=[DataRequired()])
    sold_fees = DecimalField("Quantity:",validators=[DataRequired()])
    sold_on_date = DateTimeField("Purchase Date:",validators=[DataRequired()])
    remarks = StringField("Remarks:")
    submit = SubmitField('Close')


    def validate_portfolio_item(self, field):
        if not Portfolio_Manager.query.filter_by(item_id=field.data).first():
            raise ValidationError('Invalid Portfolio Item.')

    def validate_user(self, field):
        if User.query.filter_by(id=field.data).first():
            raise ValidationError('Portfolio Item does not belong to this user.')