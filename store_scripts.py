import re
import logging
import sqlite3

from config import Config
from logging_setup import logging_setup
from send_email import send_email

products_db = Config.DB.products
orders_db = Config.DB.orders


class Product:
    @staticmethod
    def create_table():
        
        try:
            with sqlite3.connect(products_db) as conn:
                cursor = conn.cursor()
                cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT NOT NULL,
            display_name TEXT NOT NULL,
            price INTEGER NOT NULL,
            description TEXT,
            category TEXT,
            promo_price INTEGER,
            stock INTEGER,
            img_url JSON)''')
                conn.commit()
        except sqlite3.Error as e:
            logging.error(e)
            return 'failed_write'
        except Exception as e:
            logging.critical(e)
            return 'unknown_error'
    
    @staticmethod
    def create_img_table():
        try:
            with sqlite3.connect(products_db) as conn:
                cursor = conn.cursor()
                cursor.execute('''
        CREATE TABLE product_imgs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT NOT NULL,
            img_path TEXT,
            blob_img blob )''')
                conn.commit()
        except sqlite3.Error as e:
            logging.error(e)
            return 'failed_write'
        except Exception as e:
            logging.critical(e)
            return 'unknown_error'

class DBScript:
    @staticmethod
    def write_into_orders_db(user_phone_number, user_location):
        logging_setup()
        try:
            with sqlite3.connect(orders_db) as conn:
                cursor = conn.cursor()
                cursor.execute(''' INSERT INTO orders (user_phone_number, user_location) 
                               VALUES(?,?)''', (user_phone_number, user_location))
                if cursor.rowcount == 0:
                    return 'failed_write'
                return 'success_write'
        except sqlite3.OperationalError as e:
            logging.error(e)
            return 'operational_error'
        except Exception as e:
            logging.critical(e)
            return 'unknown_error'


class Order:
    @staticmethod
    def create(session):
        try:
            session['order']
            return 'success_order_create'
        except Exception as e:
            logging.critical(e)
            return 'failed_create_order'
        
    @staticmethod
    def valid_checkout_form(user_phone_number, user_location):
        logging_setup()
        try:
            phone_str = ''.join(str(user_phone_number).split())
            
            if not re.match(r'^\d{8,}$', phone_str):
                return 'invalid_phone_number'
            
            if not isinstance(user_location, str) or not user_location.strip():
                return 'invalid_location'
            
            formatted_phone = int(f"225{phone_str}")
            
            email_body = f'Numero de telephone : {formatted_phone}\n- Lieu de livraison : {user_location.strip()}'
            send_email_func = send_email(email_body)
            if send_email_func == 'success':
                return 'success_valid_checkout_form'
            else:
                return 'unknown_error'
        
        except Exception as e:
            logging.critical(f"Erreur lors de la validation du formulaire : {str(e)}")
            return 'unknown_error'
    
def view_all_orders():
    with sqlite3.connect(orders_db) as conn:
        cursor = conn.cursor()
        rows = cursor.execute('SELECT * FROM orders')
        results = rows.fetchall()
        return results
    
def read_in_logging():
    with open('logging.log', 'r') as file:
        line_list = file.readlines()
        return line_list
    

