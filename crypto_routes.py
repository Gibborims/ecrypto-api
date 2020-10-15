from flask import Flask, redirect, url_for, request
import crypto_db
# import CryptoDb from crypto_db
app = Flask(__name__)


crypto = crypto_db.CryptoDb()

@app.route('/hello/<name>')
def hello_name(name):
    return 'Hello %s!' % name

@app.route('/dob/<int:age>')
def date_of_age(age):
    return 'My age is %d' % age

@app.route('/expenses/<float:amount>')
def expenses_amt(amount):
    return 'Amount for expenses is %d' % amount

@app.route('/guests/<guest>')
def for_guests(guest):
    return 'Hello %s as Guest' % guest

@app.route('/crypto_list')
def for_cryptos():
    print(crypto.get_cryptos())
    crypto_dict = { "crypto_list" : crypto.get_cryptos() }
    return crypto_dict

@app.route('/crypto_data/<symbol>')
def for_crypto_data(symbol):
    crypt_data = crypto.get_yesterdays_price(symbol)
    print(crypt_data)
    crypto_dict = { "data" : crypt_data }
    return crypto_dict



@app.route('/admins')
def for_admins():
    return 'Hello admin..'


@app.route('/success/<name>')
def success(name):
    return 'You are welcome %s' % name

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_name = request.form['nw']
        return redirect(url_for('success', name = user_name))
    else:
        user_name = request.args.get('nw')
        return redirect(url_for('success', name = user_name))


@app.route('/roles/<role>')
def user_roles(role):
    if role == 'admin':
        return redirect(url_for('for_admins'))
    elif role == 'guest':
        return redirect(url_for('for_guests', guest = role))
    else:
        return 'This input is not a ROLE.'


if __name__ == '__main__':
    app.run(debug = True)
