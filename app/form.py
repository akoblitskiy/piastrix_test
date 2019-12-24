from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Regexp
import hashlib


class PaymentForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired()])
    currency = SelectField('Currency', validators=[DataRequired()], choices=[
        ('eur', 'EUR'),
        ('usd', 'USD'),
        ('rub', 'RUB')
    ])
    description = TextAreaField('Product info')
    submit = SubmitField('Submit')

    def __init__(self, piastrix):
        super(PaymentForm, self).__init__()
        self._piastrix = piastrix

    def generate_api_request(self, order_id):
        currency_value = self.currency.data
        if currency_value == 'eur':
            url = 'https://pay.piastrix.com/en/pay'
            action = 'pay'
            request_data = {'currency': self._piastrix.currency_ids[currency_value],
                    'amount': self.amount.data,
                    'shop_id': self._piastrix.shop_id,
                    'shop_order_id': order_id}
        elif currency_value == 'usd':
            url = 'https://core.piastrix.com/bill/create'
            action = 'bill'
            request_data = {'shop_currency': self._piastrix.currency_ids[currency_value],
                    'payer_currency': self._piastrix.currency_ids[currency_value],
                    'shop_amount': self.amount.data,
                    'shop_id': self._piastrix.shop_id,
                    'shop_order_id': order_id}
        else:
            url = 'https://core.piastrix.com/invoice/create'
            action = 'invoice'
            request_data = {'currency': self._piastrix.currency_ids[currency_value],
                    'amount': self.amount.data,
                    'payway': self._piastrix.payway,
                    'shop_id': self._piastrix.shop_id,
                    'shop_order_id': order_id}

        str_key = ''
        for key in sorted(request_data):
            if str_key:
                str_key += ':'
            str_key += str(request_data[key])
        str_key += self._piastrix.secret_key

        hex_key = hashlib.sha256(str_key.encode()).hexdigest()
        request_data['sign'] = hex_key

        return url, action, request_data
