import sys
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QMessageBox
from ModelDBCurrency import *

objModel = ModelDBCurrency()
data_table = objModel.get_all_data()

def signalConvert(self):
    self.cbToCurrency.currentTextChanged().connect(self.convert)

def window():
    app = QApplication(sys.argv)
    win = QWidget()
    cbFromCurrency = QComboBox(win)
    cbFromCurrency.move(50, 50)
    cbFromCurrency.addItem("USD")
    cbFromCurrency.addItem("IDR")
    cbFromCurrency.addItem("MYR")
    cbFromCurrency.addItem("JPY")
    win.setWindowTitle("Currency Converter")
    win.show()
    sys.exit(app.exec_())

def convert(self):
    fromCurrCode = self.cbFromCurrency.currentText()
    # fromCurrCode = "EUR"
    fromCurrInput = self.tfFromCurrency.text()
    # fromCurrInput = int("10")
    fromCurrValue = objModel.get_currency(fromCurrCode)[2]
    toCurrCode = self.cbToCurrency.currentText()
    # toCurrCode = "MYR"
    toCurrValue = objModel.get_currency(toCurrCode)[2]
    result = fromCurrInput / fromCurrValue
    # print(f"{fromCurrCode} {fromCurrInput} = {toCurrCode} ({result} x {toCurrValue}) = {result * toCurrValue}")
    return result * toCurrValue

def addCurrency(self):
    currCode = self.tfNewCurrCode.text()
    currVal = self.tfNewCurrVal.text()
    objModel.add_currency(currCode, currVal)

if __name__ == '__main__':
    window()

# def addCurrency(self):
    # currCode = self.tfNew

# convert()

# def showTable(self):
    # app = QApplication(sys.argv)
    # win = QWidget()
    # button1 = QPushButton(win)
    # button1.setText("Show dialog!")
    # button1.move(50, 50)
    # button1.clicked.connect(showDialog)
    # win.setWindowTitle("Click button")
    # win.show()
    # sys.exit(app.exec_())
