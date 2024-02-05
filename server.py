# Import necessary modules
from flask import Flask, render_template, redirect, request, jsonify
from urllib.parse import urlencode
import stripe
from mail import *
from sql import *


# Set your Stripe API key
stripe.api_key = 'sk_test_51OV2PoJNKpDwUsDXGgmoFwX4dTAJXJG2LIp5zhe8PSdRYK1f6LfkjMHsKP5okfMr77zOYicoGI6rzp2ogdDdu3kB00ZYSqpyE8'

# Create a Flask application
app = Flask(__name__,
            static_url_path='/static',
            static_folder='static')

# Define your domain (replace with your actual domain)
YOUR_DOMAIN = 'http://127.0.0.1:4242'

# Route to render the checkout template with a specific quantity


@app.route('/')
def index():
    return render_template('web.html')
@app.route('/checkout/<int:quantity>', methods=['GET'])
def checkout(quantity):
    return render_template('checkout.html', quantity=quantity)
@app.route('/process-form', methods=['GET'])
def process_form(name,lastname,mail):
    # Retrieve the quantity from the form data
    name = request.form.get('Name')
    lastname = request.form.get('Lastname')
    mail = request.form.get('Mail')

    # Process the form data and perform additional logic

    return render_template('checkout.html', name=name, lastname=lastname, mail=mail)
@app.route('/checkout.html',methods=['GET'])
def discountcode():
    # Retrieve the DiscountCode parameter from the URL
    discount_code = request.args.get('discountcode', default=None)

    # Pass the discount_code to the template or use it as needed
    return render_template('checkout.html', discountcode=discount_code)

# Route to create a checkout session
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        print(request.form)
        # Retrieve the quantity from the form data
        quantity = int(request.form.get('quantity'))
        name = request.form.get('Name')
        lastname = request.form.get('Lastname')
        mail = request.form.get('Mail')
        discount_code = request.form.get('discountcode', default=None)
        if discount_code!='':
            discount_code=[{'coupon': 'Zngxhs1A'}]
        else:
            discount_code=None
        # Create a checkout session
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1OWVNPJNKpDwUsDXFOA4nvSo',
                    'quantity': quantity,
                },
            ],
            mode='payment',
            cancel_url=f'{YOUR_DOMAIN}/cancel.html?{urlencode({"name": name, "lastname": lastname, "mail": mail})}',
            success_url=YOUR_DOMAIN + '/cancel.html',
            automatic_tax={'enabled': True},          
            discounts=discount_code,
        )
    except Exception as e:
        return str(e)

    # Redirect the user to the checkout session
    return redirect(checkout_session.url, code=303)



@app.route('/cancel.html')
def cancel():
    # Retrieve information from the query parameters
    name = request.args.get('name')
    lastname = request.args.get('lastname')
    mail = request.args.get('mail')
    send_mail(mail,name)
    insert_sql(mail,name,lastname)

    return render_template('/cancel.html', name=name, lastname=lastname, mail=mail)

@app.route('/success.html')
def success():
    return render_template('/success.html')


@app.route('/checkEmail/<email>', methods=['GET'])
def check_email(email):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()

        # Execute a SELECT query to check if the email exists
        cursor.execute('SELECT COUNT(*) FROM contacts WHERE email = ?', (email,))
        count = cursor.fetchone()[0]

        # Close the connection
        conn.close()

        # Return JSON response indicating if the email exists
        return jsonify({'exists': count > 0})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Run the application on port 4242
if __name__ == '__main__':
    app.run(debug=True, port=4242)
