#!/usr/bin/python
#-*- coding: utf-8 -*-
#
# KCnrtl is a simple and messy KDE graphical client to access
# the CNRTL linguistic resources
#
# Copyright (C) 2012 Bogdan Cordier
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys
import httplib2
from bs4 import BeautifulSoup
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from gui.Ui_kcnrtl import Ui_MainWindow
import re
import shutil


def main():
    app = QApplication(sys.argv)
    myapp = Main()
    myapp.show()
    sys.exit(app.exec_())


class Main(QMainWindow):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        #QWidget.__init__(self, parent)

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        self.ui.lineEdit.selectAll()

        self.ui.lineEdit.setFocus()

        self.ui.comboBox.setCurrentIndex(0)

        self.ui.checkBox.setChecked(False)

        self.clipboard = QApplication.clipboard()

        self.ui.lineEdit.returnPressed.connect(self.updateUi)

        self.ui.comboBox.activated.connect(self.changeCombo)
        
        self.ui.webView.settings().setUserStyleSheetUrl(
                                               QUrl.fromLocalFile(":/lexi.css"))

        self.ui.listView.clicked.connect(self.rowClicked)

        self.clipboard.dataChanged.connect(self.autoGetFromClipboard)

    def updateUi(self):
        try:
            # Check if input text is a word
            if len(unicode(self.ui.lineEdit.text()).split()) <= 1:
                self.typed = unicode(self.ui.lineEdit.text())
                self.getLexi(self.typed)
                self.ui.comboBox.clear()
                self.ui.comboBox.addItems(self.lexiForm())
                self.lexiContent()
                self.ui.listView.setModel(self.getSynoAnto("synonymie"))
                self.ui.listView_2.setModel(self.getSynoAnto("antonymie"))
            else:
                self.ui.lineEdit.setText("Veuillez entrer UN mot")

        except:
            self.ui.lineEdit.setText("Veuillez entrer un mot")

    # Copy selected item in list to the clipboard
    def rowClicked(self, qmodelindex):
        self.item = qmodelindex.data(Qt.DisplayRole).toString()
        self.clipboard.setText(self.item)

    def autoGetFromClipboard(self):
        if self.ui.checkBox.isChecked():
            self.ui.lineEdit.setText(unicode(self.clipboard.text()))
            self.updateUi()

    def changeCombo(self):
        self.getLexi(self.typed)
        self.lexiContent()
    
    def getSynoAnto(self, form):
        tag = []
        soup = BeautifulSoup(self.getHtml(self.typed, form))
        tagy = soup.find_all('td', "%s_format" % (form[:4]))
        i = 0
        while i < len(tagy):
            tag_a = tagy[i]
            tag.append(tag_a.text)
            i += 1
        model = ListModel(tag, self)
        return model
     
    def getLexi(self, text):
        h = self.getHtml(text, "definition")
        global soup
        soup = BeautifulSoup(h, "lxml")
        return soup

    def lexiContent(self):
        tagy = soup.find_all('div', {'id': 'contentbox'})
        tag = str(tagy[0])
        self.ui.webView.setHtml(tag.decode('utf8'))
        return tagy

    # Recupere les differentes formes
    def lexiForm(self):
        a = re.compile("return sendRequest\(5,'/definition/.*")
        multdef = soup.find_all('a', {'onclick': a})
        tagform = []
        i = 0
        while i < len(multdef):
            multdef_a = multdef[i]
            # Suppression des chiffres présents dans la chaîne
            multdef_clean = ''.join(c for c in
                                    multdef_a.text if not c.isdigit())
            # Ajout de chaque chaîne à la liste tagform
            tagform.append(multdef_clean)
            i += 1
        return tagform

    def getHtml(self, text, form):
        conn = httplib2.Http(".cache")
        numdef = self.ui.comboBox.currentIndex()
        if form == "definition":
            htmlSource = conn.request("http://www.cnrtl.fr/%s/%s//%s" %
                                        (form, text, numdef), "GET")
        else:
            htmlSource = conn.request("http://www.cnrtl.fr/%s/%s" %
                                        (form, text), "GET")
        return htmlSource[1]
        
    # Delete cache directory on close
    def closeEvent(self, event):
        shutil.rmtree('.cache')
        print "closed"

class ListModel(QAbstractListModel):
    def __init__(self, datain, parent=None, *args):
        """ datain: a list where each item is a row
        """
        QAbstractListModel.__init__(self, parent, *args)
        self.listdata = datain

    def rowCount(self, parent=QModelIndex()):
        return len(self.listdata)

    def data(self, index, role):
        if index.isValid() and role == Qt.DisplayRole:
            return QVariant(self.listdata[index.row()])
        else:
            return QVariant()

if __name__ == "__main__":
    main()
