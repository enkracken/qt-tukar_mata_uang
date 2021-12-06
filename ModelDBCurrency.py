import sqlite3, requests, json

class ModelDBCurrency:

    def __init__(self):
        self.__db = sqlite3.connect('currency.db')
        self.__cursor = self.__db.cursor()


    def start_currency_db(self):
        try:
            self.__cursor.execute('''
                CREATE TABLE IF NOT EXISTS currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                currency_code CHAR NOT NULL,
                currency_value INTEGER NOT NULL);
            ''')
            self.__cursor.execute("CREATE UNIQUE INDEX idx_currency_code ON currency (currency_code);")
            print("tabel currency berhasil dibuat")
        except sqlite3.Error as error:
            print("gagal membuat table", error)

    def set_all_data(self):# jangan panggil fungsi ini, kecuali sekali di awal. Ntar batas penggunaan gw abis
        try:
            self.__url = "https://freecurrencyapi.net/api/v2/latest?apikey=5434dc70-5507-11ec-b7e9-c7d770891d9a"    
            self.__response = requests.get(self.__url)
            self.__hasil = json.loads(self.__response.text)
            if len(self.__hasil["data"].items()) != 0:
                records = ""
                forCount = 0
                for curr_code, curr_val in self.__hasil["data"].items():
                    forCount += 1
                    records += f" ('{curr_code}', '{str(curr_val)}')"
                    if forCount < len(self.__hasil["data"].items()):
                        records += ","

                self.__cursor.execute("DELETE FROM currency;")
                self.__cursor.execute("DELETE FROM sqlite_sequence WHERE name='currency';")
                self.__cursor.execute(f"INSERT INTO currency (currency_code, currency_value) VALUES ('{self.__hasil['query']['base_currency']}', 1);")
                self.__cursor.execute(f"INSERT INTO currency (currency_code, currency_value) VALUES{records};")
                self.__db.commit()
                del records
                del forCount
            else:
                print("No data in response. Your limit request has been reached.")
        except:
            print("Can't connect to API.")

    def get_all_data(self):
        result = list(self.__cursor.execute("SELECT * FROM currency;"))
        # for row in result:
        #     print(row)
        return result

    def set_currency(self, curr_code, curr_val):
        self.__cursor.execute(f"UPDATE currency SET currency_value = {curr_val} WHERE currency_code = '{curr_code}';")
        if self.__cursor.rowcount == 0:
            self.__cursor.execute(f"INSERT INTO currency (currency_code, currency_value) VALUES('{curr_code}', '{curr_val}');")

    def add_currency(self, curr_code, curr_val):
        try:
            self.__cursor.execute(f"INSERT INTO currency (currency_code, currency_value) VALUES('{curr_code}', '{curr_val}');")
        except sqlite3.Error as error:
            print("Gagal. Duplikat kode mata uang.", error)

    def update_currency(self, curr_code, curr_val):
        try:
            self.__cursor.execute(f"UPDATE currency SET currency_value = {curr_val} WHERE currency_code = '{curr_code}';")
        except sqlite3.Error as error:
            print(f"Gagal. {curr_code} tidak ditemukan", error)

    def get_currency(self, curr_code):
        # print(f"SELECT * FROM currency WHERE currency_code = '{curr_code}';")
        return list(self.__cursor.execute(f"SELECT * FROM currency WHERE currency_code = '{curr_code}';"))[0]

    def get_base_currency(self):
        return list(self.__cursor.execute(f"SELECT * FROM currency WHERE id = 1;"))[0][1]

model1 = ModelDBCurrency()
# model1.start_currency_db()
# model1.set_all_data()
# print(model1.get_currency("IDR"))
# print(model1.get_base_currency())
# model1.get_all_data()

# {
#     "query":{
#         "apikey":"5434dc70-5507-11ec-b7e9-c7d770891d9a",
#         "timestamp":1638625819,
#         "base_currency":"USD"
#     },
#     "data":{
#         "JPY":112.80268,
#         "CNY":6.37264,
#         "CHF":0.91777,
#         "CAD":1.28436,
#         "MXN":21.2756,
#         "INR":75.22571,
#         "BRL":5.64657,
#         "RUB":73.73825,
#         "KRW":1176.93065,
#         "IDR":14395.16857,
#         "TRY":13.6478,
#         "SAR":3.75134,
#         "SEK":9.14077,
#         "NGN":409.73735,
#         "PLN":4.05941,
#         "ARS":101.05149,
#         "NOK":9.18247,"TWD":27.65638,"IRR":42001.1356,"AED":3.67276,"COP":3963.47178,"THB":33.84064,"ZAR":16.06616,"DKK":6.57239,
#         "MYR":4.2291,"SGD":1.37134,"ILS":3.16029,"HKD":7.79403,"EGP":15.66019,"PHP":50.41091,"CLP":840.39366,"PKR":176.35225,
#         "IQD":1458.03263,"DZD":138.62381,"KZT":438.24198,"QAR":3.64155,"CZK":22.4845,"PEN":4.06908,"RON":4.3721,"VND":22830.50626,
#         "BDT":85.44246,"HUF":321.51922,"UAH":27.33043,"AOA":582.42617,"MAD":9.22824,"OMR":0.38491,"CUC":24.00062,"BYR":3.00005,
#         "AZN":1.69303,"LKR":201.00362,"SDG":436.33668,"SYP":2510.05863,"MMK":1776.54607,"DOP":56.47082,"UZS":10760.16505,
#         "KES":112.60242,"GTQ":7.72812,"URY":44.15069,"HRV":6.67338,"MOP":8.02819,"ETB":48.04956,"CRC":628.89124,"TZS":2298.04493,
#         "TMT":3.49007,"TND":2.88058,"PAB":1.00003,"LBP":1504.03101,"RSD":103.8915,"LYD":4.58342,"GHS":6.03009,"YER":249.70626,
#         "BOB":6.82013,"BHD":0.37691,"CDF":1966.55853,"PYG":6797.15326,"UGX":3560.20624,"SVC":8.74134,"TTD":6.75837,
#         "AFN":95.9827,"NPR":120.26279,
#         "HNL":24.10769,"BIH":1.72975,"BND":1.37183,"ISK":129.46172,"KHR":4063.08169,"GEL":3.08696,"MZN":63.20147,"BWP":11.70979,"PGK":3.5418,
#         "JMD":154.04183,"XAF":579.38886,"NAD":16.07038,"ALL":106.8219,"SSP":406.47077,"MUR":42.85103,"MNT":2831.06931,"NIO":35.21075,
#         "LAK":10879.2307,"MKD":54.47081,"AMD":488.00807,"MGA":3955.057,"XPF":105.23188,"TJS":11.28026,"HTG":98.00218,"BSD":1.00002,
#         "MDL":17.63251,"RWF":1022.02504,"KGS":84.79234,"GNF":9315.19237,"SRD":21.40849,"SLL":11025.11697,"XOF":578.30761,
#         "MWK":807.30165,"FJD":2.12736,"ERN":15.00037,"SZL":16.0702,"GYD":207.77272,"BIF":1984.82572,"KYD":0.82502,
#         "MVR":15.42032,"LSL":16.06536,"LRD":141.00297,"CVE":97.48247,"DJF":177.50402,"SCR":14.51561,"SOS":575.01298,
#         "GMD":52.40057,"KMF":435.6063,"STD":21.67026,"XRP":1.07003,"AUD":1.42894,
#         "BGN":1.73393,
#         "BTC":0.0186,
#         "JOD":0.70802,
#         "GBP":0.75542,
#         "ETH":0.00024,
#         "EUR":0.88421,
#         "LTC":0.01,
#         "NZD":1.48163
#     }
# }
