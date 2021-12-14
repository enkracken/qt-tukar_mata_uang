from UI_Converter import *
from UI_Table import *
from ModelMariaDBCurrency import *
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *

objModel = ModelMariaDBCurrency()
objModel.start_currency_db()

def signalsConverter(self):
    # UI manipulation
    self.btSwap.setIcon(QIcon("exchange-icon.png"))
    self.tfFromCurrency.setButtonSymbols(QAbstractSpinBox.NoButtons)
    self.tfBlocker = QtCore.QSignalBlocker(self.tfFromCurrency)
    self.tfBlocker.unblock()
    self.cbfBlocker = QtCore.QSignalBlocker(self.cbFromCurrency)
    self.cbfBlocker.unblock()
    self.cbtBlocker = QtCore.QSignalBlocker(self.cbToCurrency)
    self.cbtBlocker.unblock()
    for row in objModel.get_all_data():
        self.cbFromCurrency.addItem(row[1])
        self.cbToCurrency.addItem(row[1])
    # Add signals
    self.tfFromCurrency.textChanged.connect(self.convert)
    self.cbToCurrency.currentTextChanged.connect(self.convert)
    self.cbFromCurrency.currentTextChanged.connect(self.convert)
    self.btRefresh.clicked.connect(self.refreshConverter)
    self.btShowTable.clicked.connect(self.showTable)
    self.btSwap.clicked.connect(self.exchange)

def signalsTable(self):
    # UI manipulation
    self.updateTable()
    self.tfCurrencyValue.setButtonSymbols(QAbstractSpinBox.NoButtons)
    self.tableWidget.setColumnWidth(0, 150)
    self.tableWidget.setColumnWidth(1, 550)
    # Add signals
    self.btSave.clicked.connect(self.setCurrency)
    self.tableWidget.itemClicked.connect(self.setCurrInputs)
    self.btUpdateDB.clicked.connect(self.updateDB)
    self.btDelete.clicked.connect(self.deleteCurrency)

def showTable(self):
    Ui_TableWidget.signalsTable = signalsTable
    Ui_TableWidget.updateTable = updateTable
    Ui_TableWidget.setCurrency = setCurrency
    Ui_TableWidget.setCurrInputs = setCurrInputs
    Ui_TableWidget.deleteCurrency = deleteCurrency
    Ui_TableWidget.updateDB = updateDB
    self.tableWindow = QtWidgets.QWidget()
    self.uiTable = Ui_TableWidget()
    self.uiTable.setupUi(self.tableWindow)
    self.uiTable.signalsTable()
    self.tableWindow.show()

def convert(self):
    fromCurrCode = self.cbFromCurrency.currentText()
    fromCurrInput = self.tfFromCurrency.value()
    fromCurrValue = objModel.get_currency(fromCurrCode)
    if fromCurrValue != 0:
        toCurrCode = self.cbToCurrency.currentText()
        toCurrValue = objModel.get_currency(toCurrCode)[2]
        result = "{:.2f}".format(float(fromCurrInput) / fromCurrValue[2] * toCurrValue)
        self.tfConvertResult.setText(result.replace('.',','))

def exchange(self):
    fromCurrCode = self.cbFromCurrency.currentText()
    fromCurrInput = self.tfFromCurrency.value()
    toCurrCode = self.cbToCurrency.currentText()
    resultValue = self.tfConvertResult.text().replace(',','.')
    self.cbFromCurrency.setCurrentText(toCurrCode)
    self.cbToCurrency.setCurrentText(fromCurrCode)
    self.tfFromCurrency.setValue(float(resultValue))
    self.tfConvertResult.setText(str(fromCurrInput).replace('.',','))

def updateTable(self):
    # mereset isi table menjadi kosong
    self.tableWidget.setRowCount(0)
    # Mulai masukkan data ke table
    for row_number, item in enumerate(objModel.get_all_data()):
        self.tableWidget.insertRow(row_number)
        self.tableWidget.setItem(row_number, 0, QtWidgets.QTableWidgetItem(str(item[1]).replace('.',',')))
        self.tableWidget.setItem(row_number, 1, QtWidgets.QTableWidgetItem(str(item[2]).replace('.',',')))
    # Buat isi table tidak bisa di-edit
    self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

def setCurrency(self):
    currCode = self.tfCurrencyCode.text()
    currVal = self.tfCurrencyValue.text().replace(',','.')
    if len(currCode) == 3 and currCode.isupper():
        if float(currVal) > 0:
            showDialog(objModel.set_currency(currCode, currVal.replace(',','.')))
            self.updateTable()
        else:
            showDialog("Nilai mata uang harus lebih dari 0.")
            self.tfCurrencyValue.setFocus()
    else:
        showDialog("Kode mata uang harus berisi 3 karakter dan menggunakan huruf kapital.")
        self.tfCurrencyCode.setFocus()

def deleteCurrency(self):
    currCode = self.tfCurrencyCode.text()
    showDialog(objModel.delete_currency(currCode))
    self.updateTable()

def updateDB(self):
    showDialog(objModel.set_all_data())
    self.updateTable()

def showDialog(message):
    msgBox = QMessageBox()
    msgBox.setText(message)
    msgBox.exec()

def refreshConverter(self):
    # Hentikan signal yang mengganggu
    self.tfBlocker.reblock()
    self.cbfBlocker.reblock()
    self.cbtBlocker.reblock()
    # Bersihkan semua item dari combobox
    self.cbFromCurrency.clear()
    self.cbToCurrency.clear()
    # Masukkan kembali item ke combobox, termasuk item yg baru saja hadir
    for item in objModel.get_all_data():
        self.cbFromCurrency.addItem(item[1])
        self.cbToCurrency.addItem(item[1])
    # Kosongkan semua text field atau line edit atau QDoubleSpinBox
    self.tfConvertResult.setText("0,00")
    self.tfFromCurrency.setValue(float(0.0))
    # Nyalakan kembali sinyal yang tadi mengganggu
    self.tfBlocker.unblock()
    self.cbfBlocker.unblock()
    self.cbtBlocker.unblock()
    showDialog("Berhasil me-refresh UI")

def setCurrInputs(self):
    selectedColumn = self.tableWidget.currentColumn()
    selectedRow = self.tableWidget.currentRow()
    cellText = self.tableWidget.currentItem().text()
    # Jika kolom yg aktif adalah kode mata uang
    if selectedColumn == 0:
        # input kode mata uang diisi dengan data di sel yg dipilih
        self.tfCurrencyCode.setText(cellText)
        # input nilai mata uang diisi data di kolom nilai mata uang, di baris yg dipilih
        self.tfCurrencyValue.setValue(float(self.tableWidget.item(selectedRow, 1).text().replace(',','.')))
    # jika kolom yg aktif adalah nilai mata uang, maka lakukan sebaliknya
    else:
        # input kode mata uang diisi data di kolom kode mata uang, di baris yg dipilih
        self.tfCurrencyCode.setText(self.tableWidget.item(selectedRow, 0).text())
        # input nilai mata uang diisi dengan data di sel yg dipilih
        self.tfCurrencyValue.setValue(float(cellText.replace(',','.')))

Ui_ConverterWidget.signals = signalsConverter
Ui_ConverterWidget.convert = convert
Ui_ConverterWidget.showTable = showTable
Ui_ConverterWidget.refreshConverter = refreshConverter
Ui_ConverterWidget.exchange = exchange

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ConverterWindow = QtWidgets.QWidget()
    ui = Ui_ConverterWidget()
    ui.setupUi(ConverterWindow)
    ui.signals()
    ConverterWindow.show()
    sys.exit(app.exec_())