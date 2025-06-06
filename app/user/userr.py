import logging
import secrets
from urllib.parse import urlencode

from flask import Blueprint, redirect, url_for, render_template, request, flash

from store_scripts import Order, view_all_orders, read_in_logging

user = Blueprint('user', __name__, template_folder='users_templates', static_folder='user_static')


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

@user.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'GET':
        # Afficher le formulaire de livraison avec les infos produit
        storage = request.args.get('storage', '10g')
        quantity = request.args.get('quantity', '1')
        return render_template('checkout.html', storage=storage, quantity=quantity)

    # POST: soumission du formulaire de livraison
    storage = request.form.get('storage', '10g')
    quantity = request.form.get('quantity', '1')
    phone = request.form.get('user_phone_number', '')
    location = request.form.get('user_location', '')

    # Validation
    result = Order.valid_checkout_form(phone, location, storage, quantity)
    if result == 'success_valid_checkout_form':
        return redirect(url_for('user.success', storage=storage, quantity=quantity, phone=phone, location=location))

    # Gestion des erreurs
    if result == 'invalid_phone_number':
        flash('Numéro de téléphone invalide.')
    elif result == 'invalid_location':
        flash('Lieu de livraison invalide.')
    else:
        flash('Une erreur est survenue. Veuillez réessayer.')

    return redirect(url_for('user.checkout', storage=storage, quantity=quantity))

@user.route('/success')
def success():
    storage = request.args.get('storage')
    quantity = request.args.get('quantity')
    phone = request.args.get('phone')
    if not storage or not quantity or not phone:
        return redirect(url_for('user.product'))

    # Calcul du prix total
    variation_prices = {'10g': 25000, '20g': 35000, '50g': 75000, '100g': 140000}
    total_price = variation_prices.get(storage, 25000) * int(quantity)

    return render_template('success.html',
                           product_name="Pierre noire de l'Inde",
                           product_format=storage,
                           quantity=quantity,
                           total_price=total_price,
                           phone=phone,
                           location=request.args.get('location', ''))