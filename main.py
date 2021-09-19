import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QHBoxLayout, QLabel
import csv
from requestshtml.getdata import Parsing_data
from ui.mainui import Ui_Dialog


class choosefunction(QtWidgets.QMainWindow):

    work_log = pyqtSignal(str)
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.comboBox.addItems(["10","50","100","150","200","250"])
        # 设置提交按钮点击事件
        self.ui.Searchbutton.clicked.connect(self.my_run)
        self.ui.Download1.clicked.connect(self.Download1)
        self.ui.Download2.clicked.connect(self.Download2)
        self.flag = 1
        self.result = []
        self.work_log.connect(self.on_log)

    def on_log(self,info):
        # print(info)
        self.ui.listWidget.addItem(info)

    def my_run(self):
        self.result = []
        self.keywords = self.ui.jobtitleedit.text()

        if self.keywords == "":
            QMessageBox.critical(
                self,
                'err',
                'Fill in the key words')
        else:
            self.num = int(self.ui.comboBox.currentText())
            for i in range(10,self.num+10,10):
                self.result += Parsing_data(self.keywords,i, self.flag,self.work_log)
            # print(self.result)
        self.work_log.emit("end")

    def Download1(self):
        if len(self.result) > 0:
            file = QFileDialog.getExistingDirectory(self, 'save file', 'C://')
            filename = str(file)+"a.csv"
            # print(filename)
            self.work_log.emit(filename+"  save successful")
            with open(filename, 'w',newline='',encoding='utf-8') as f:
                # headers = ['Number of jobs:', self.num]
                f_csv = csv.writer(f)
                # f_csv.writerow(headers)
                f_csv.writerow(["Number of jobs:","Job titles","Job Descriptions","Company Names","URLs"])
                f_csv.writerows(self.result)
        else:
            QMessageBox.critical(
                self,
                'err',
                'no data')
    def Download2(self):
        if len(self.result) > 0:
            file = QFileDialog.getExistingDirectory(self, 'save file', 'C://')
            filename = str(file)+"b.csv"
            resu = []
            for i in self.result:
                resu.append([i[0],i[2]])
            # print(filename)
            self.work_log.emit(filename+"  save successful")
            with open(filename, 'w',newline='',encoding='utf-8') as f:
                f_csv = csv.writer(f)
                f_csv.writerow(["Number of Jobs","Job Descriptions"])
                f_csv.writerows(resu)
        else:
            QMessageBox.critical(
                self,
                'err',
                'no data')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win_main = choosefunction()
    win_main.show()
    sys.exit(app.exec_())
