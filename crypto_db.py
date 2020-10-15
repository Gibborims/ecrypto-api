import psycopg2
from psycopg2.extras import RealDictCursor
import sys

def print_err(err):
    print(str(err) + " on line " + str(sys.exc_info()[2].tb_lineno))

def print_text():
    print('Well done to this point...')

class CryptoDb:
    def __init__(self):
        pwd = "test123"
        host = "localhost"
        self.conn = psycopg2.connect("dbname=grayscale_db user=francis password={} host={}".format(pwd,host))
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)

    def get_cryptos(self):
        self.cur.execute("SELECT * FROM cryptos;")
        data = self.cur.fetchall()
        return data

    def get_crypto_by_symbol(self,symbol):
        self.cur.execute("SELECT * FROM cryptos WHERE symbol = %s",[symbol])
        crypto = self.cur.fetchone()
        if crypto:
            return crypto

    def create_price(self, symbol, price):
        crypto = self.get_crypto_by_symbol(symbol)
        print("creating price...")
        print("symbol: ", symbol, "crypto: ", crypto)
        if crypto:
            self.cur.execute("SELECT * FROM prices WHERE crypto_id = %s AND created_at::DATE = CURRENT_DATE",[crypto["id"]])
            if self.cur.fetchone():
                print("Data already inserted")
            else:
                self.cur.execute("INSERT INTO prices (crypto_id, price) VALUES (%s, %s)",[crypto["id"], price])
                self.conn.commit()

    def get_yesterdays_price(self, symbol):
        crypto = self.get_crypto_by_symbol(symbol)
        print("symbol: ",symbol,' CRYPTO: ', crypto)
        if crypto:
            self.cur.execute("SELECT * FROM prices WHERE crypto_id = %s AND created_at BETWEEN CURRENT_DATE - INTERVAL '1 day' AND CURRENT_DATE",[crypto["id"]])
            data = self.cur.fetchone()
            return data

