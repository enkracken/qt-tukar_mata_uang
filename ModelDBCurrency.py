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
                currency_value REAL NOT NULL);
            ''')
        except sqlite3.Error as error:
            print("gagal membuat table", error)
            return f"gagal membuat table. {error}"

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
                        records += "," # ini nambahin koma di akhir yg dalam kurung itu ("KODE", 122), yang koma terakhir

                self.__cursor.execute("DELETE FROM currency;")
                self.__cursor.execute("DELETE FROM sqlite_sequence WHERE name='currency';")
                self.__cursor.execute(f"INSERT INTO currency (currency_code, currency_value) VALUES ('{self.__hasil['query']['base_currency']}', 1);")
                self.__cursor.execute(f"INSERT INTO currency (currency_code, currency_value) VALUES{records};")
                self.__db.commit()
                del records
                del forCount
                print("Database berhasil di-update menggunakan data dari API")
                return "Database berhasil di-update menggunakan data dari API"
            else:
                print("Tidak ada data di response. Batas penggunaan API mungkin sudah tercapai.")
                return "Tidak ada data di response. Batas penggunaan API mungkin sudah tercapai."
        except:
            print("Tidak bisa terhubung ke API.")
            return "Tidak bisa terhubung ke API."

    def get_all_data(self):
        return list(self.__cursor.execute("SELECT * FROM currency;"))

    def set_currency(self, curr_code, curr_val):
        try:
            self.__cursor.execute(f"UPDATE currency SET currency_value = '{curr_val}' WHERE currency_code = '{curr_code}';")
            if self.__cursor.rowcount == 0:
                self.__cursor.execute(f"INSERT INTO currency (currency_code, currency_value) VALUES('{curr_code}', '{curr_val}');")
                self.__db.commit()
                return f"Berhasil menginput data {curr_code}"
            else:
                self.__db.commit()
                return f"Berhasil mengubah nilai {curr_code}"
        except sqlite3.Error as error:
            return f"Gagal memasukkan data {error}"

    def get_currency(self, curr_code):
            result = list(self.__cursor.execute(f"SELECT * FROM currency WHERE currency_code = '{curr_code}';"))
            if len(result) != 0:
                return result[0]
            else:
                return 0
    
    def delete_currency(self, curr_code):
        try:
            self.__cursor.execute(f"DELETE FROM currency WHERE currency_code = '{curr_code}'")
            return "Data berhasil di hapus"
        except sqlite3.Error as error:
            return error
