import logging
import secrets

from flask import Blueprint, redirect, url_for, render_template, request, flash, session

from store_scripts import Order, view_all_orders, read_in_logging

user = Blueprint('user', __name__, template_folder='users_templates', static_folder='user_static')

@user.before_request
def make_session_permanent():
        session.permanent = True


@user.route('/')
def index():
    return redirect(url_for('user.product'))

@user.route('/<code>')
def redirect_404(code):
    if code:
        return redirect(url_for('user.index'))
    else:
        return redirect(url_for('user.index'))
    
@user.route('/product')
def product():
    return render_template('product.html')

@user.route('/create_order', methods=['POST'])
def create_order():
    if request.method == 'POST' and 'order_btn' in request.form:
        return redirect(url_for('user.checkout') )
    return redirect(url_for('user.product'))
    

@user.route('/checkout', methods=['GET', 'POST'])
def checkout():
    session['success_checkout'] = 'success_checkout'
    if request.method == 'POST' and 'checkout_btn' in request.form:
        session['create_order'] = 'create_order'

        user_phone_number = request.form['user_phone_number'] if request.form['user_phone_number'] else None
        user_location = request.form['user_location'] if request.form['user_location'] else None
        session['user_phone_number'] = user_phone_number
        session['user_location'] = user_location

        valid_checkout_form_response = Order.valid_checkout_form(user_phone_number, user_location)
        
        if valid_checkout_form_response == 'unknown_error':
            flash('')
            redirect(url_for('user.checkout'))
        elif valid_checkout_form_response == 'user_phone_number_not_int':
            flash('')
            redirect(url_for('user.checkout'))
        elif valid_checkout_form_response == 'user_location_not_valid':
            flash('')
            redirect(url_for('user.checkout'))
        elif valid_checkout_form_response == 'success_valid_checkout_form':
            session['success_checkout'] = 'success_checkout'
            return redirect(url_for('user.success'))
        return redirect(url_for('user.checkout'))
    
    user_phone_number = session.get('user_phone_number') or ''
    user_location = session.get('user_location') or ''
    return render_template('checkout.html', user_phone_number=user_phone_number, user_location=user_location)

@user.route('/success', methods=['GET'])
def success():
    if 'success_checkout' in session:
        session.clear()
        return render_template('success.html')
    return redirect(url_for('user.product'))