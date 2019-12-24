from app import app
from flask import render_template, flash, redirect, request, jsonify

from app.dbmodel import Database
from app.form import PaymentForm
from app.piastrix import Piastrix


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    piastrix = Piastrix()
    form = PaymentForm(piastrix)
    if form.validate_on_submit():
        database = Database()
        order_id = database.get_order_id()
        if not order_id:
            order_id = 1
        url, action, data = form.generate_api_request(order_id)

        if action == 'pay':
            database.write_payment(data['shop_order_id'], data['currency'], data['amount'], form.description.data, 'ok')
            return render_template('payform.html', title='Payment form', url=url, data=data)
        elif action == 'bill':
            piastrix.proceed_bill(url, data)
            database.write_payment(data['shop_order_id'], data['currency'], data['amount'], form.description.data,
                                   piastrix.response['error']['message'] if 'error' in piastrix.response else 'ok')
            if 'error' in piastrix.response:
                return jsonify(piastrix.response)
            else:
                return redirect(piastrix.response['url'])
        elif action == 'invoice':
            piastrix.proceed_invoice(url, data)
            database.write_payment(data['shop_order_id'], data['currency'], data['amount'], form.description.data,
                                   piastrix.response['error']['message'] if 'error' in piastrix.response else 'ok')
            if 'error' in piastrix.response:
                return jsonify(piastrix.response)
            else:
                return render_template('invoiceform.html', title='Invoice form', url=piastrix.response['url'],
                                       data=piastrix.response['data'])

    return render_template('form.html', title='Payment form', form=form)
