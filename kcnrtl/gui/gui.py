#!/usr/bin/python
#-*- coding: utf-8 -*-

########################################################################
# This file is part of KCnrtl                                          #
#                                                                      #
#                                                                      #
# Copyright (C) 2012 Bogdan Cordier                                    #
#                                                                      #
# KCnrtl is free software: you can redistribute it and/or modify       #
# it under the terms of the GNU General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or    #
# (at your option) any later version.                                  #
#                                                                      #
# KCnrtl is distributed in the hope that it will be useful,            #
# but WITHOUT ANY WARRANTY; without even the implied warranty of       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        #
# GNU General Public License for more details.                         #
#                                                                      #
# You should have received a copy of the GNU General Public License    #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.#
########################################################################

import sys
from PyQt4.QtCore import QUrl, Qt
from PyQt4.QtGui import  QApplication, QMainWindow, QWidget
from kcnrtl.fetchparseqt import FetchParse
from kcnrtl.models import ListModel
from kcnrtl.gui.Ui_kcnrtl import Ui_MainWindow


def main():
    app = QApplication(sys.argv)
    myapp = Main()
    myapp.show()
    sys.exit(app.exec_())


class Main(QMainWindow):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        
        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        self.ui.lineEdit.selectAll()

        self.ui.lineEdit.setFocus()

        self.ui.comboBox.setCurrentIndex(0)

        self.ui.checkBox.setChecked(False)


        self.dictionaries = [str("TLFi").decode("utf-8", "strict"),
                             str("Académie 9e Ed.").decode("utf-8", "strict"),
                             str("Académie 8e Ed.").decode("utf-8", "strict"),
                             str("Académie 4e Ed.").decode("utf-8", "strict"),
                                ]
        self.ui.comboBox_2.addItems(self.dictionaries)
        
        self.clipboard = QApplication.clipboard()

        self.ui.lineEdit.returnPressed.connect(self.update_ui)

        self.ui.comboBox.activated.connect(self.on_combo_change)
        
        self.ui.webView.settings().setUserStyleSheetUrl(
                                               QUrl.fromLocalFile(':/lexi.css'))

        self.ui.listView.clicked.connect(self.on_row_clicked)

        self.clipboard.dataChanged.connect(self.get_from_clipboard)



    def update_ui(self):
        # Check if input text is a word
        """
        Update the ui when a new word is entered.
        """
        if len(unicode(self.ui.lineEdit.text()).split()) <= 1:
            wordclass = "definition"
            dico = "Lexi"
            lexi = FetchParse(self.ui.lineEdit.text(), dico, self.ui.comboBox.currentIndex(),
                self.ui.comboBox_2.currentIndex(), self.ui.comboBox_2.currentText(), wordclass)
            result_lexi = lexi.reply
            self.ui.webView.setHtml(result_lexi[0])
            self.ui.comboBox.clear()
            self.ui.comboBox.addItems(result_lexi[1])
            wordclass = "synonyme"
            dico = "Syno"
            syno = FetchParse(self.ui.lineEdit.text(), dico, self.ui.comboBox.currentIndex(),
                self.ui.comboBox_2.currentIndex(), self.ui.comboBox_2.currentText(), wordclass)
            model = ListModel(syno.reply, self)
            self.ui.listView.setModel(model)
            wordclass = "antonyme"
            dico = "Anto"
            anto = FetchParse(self.ui.lineEdit.text(), dico, self.ui.comboBox.currentIndex(),
                self.ui.comboBox_2.currentIndex(), self.ui.comboBox_2.currentText(), wordclass)
            model = ListModel(anto.reply, self)
            self.ui.listView_2.setModel(model)

        else:
            self.ui.lineEdit.setText("Veuillez entrer UN mot")

    def on_row_clicked(self, qmodelindex):
        """
        Copy selected item in list to the clipboard.
        """
        item = qmodelindex.data(Qt.DisplayRole).toString()
        self.clipboard.setText(item)
#
    def get_from_clipboard(self):
        """
        Pass clipboard content as a new word and update ui.
        """
        if self.ui.checkBox.isChecked():
            self.ui.lineEdit.setText(unicode(self.clipboard.text()))
            self.update_ui()
#
    def on_combo_change(self):
        wordclass = "definition"
        dico = "Lexi"
        lexi = FetchParse(self.ui.lineEdit.text(), dico, self.ui.comboBox.currentIndex(),
            self.ui.comboBox_2.currentIndex(), self.ui.comboBox_2.currentText(), wordclass)
        result_lexi = lexi.reply
        self.ui.webView.setHtml(result_lexi[0])

if __name__ == "__main__":
    main()
