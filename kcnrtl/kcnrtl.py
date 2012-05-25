#!/usr/bin/python
#-*- coding: utf-8 -*-

########################################################################
# KCnrtl - A simple Qt graphical client to access the CNRTL            #
# french linguistic resources.                                         #
#                                                                      #
# Copyright (C) 2012 Bogdan Cordier                                    #
#                                                                      #
# This program is free software: you can redistribute it and/or modify #
# it under the terms of the GNU General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or    #
# (at your option) any later version.                                  #
#                                                                      #
# This program is distributed in the hope that it will be useful,      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of       #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        #
# GNU General Public License for more details.                         #
#                                                                      #
# You should have received a copy of the GNU General Public License    #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.#
########################################################################

import sys
from PyQt4.QtCore import QEventLoop, QUrl, QAbstractListModel, QModelIndex, QVariant, Qt
from PyQt4.QtGui import  QApplication, QMainWindow, QWidget
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt4.QtWebKit import QWebPage
from gui.Ui_kcnrtl import Ui_MainWindow


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

        self.manager = QNetworkAccessManager()
                
        self.dictionaries = [str("TLFi").decode("utf-8", "strict"),
                             str("Académie 9e Ed.").decode("utf-8", "strict"),
                             str("Académie 8e Ed.").decode("utf-8", "strict"),
                             str("Académie 4e Ed.").decode("utf-8", "strict"),
                                ]
        self.ui.comboBox_2.addItems(self.dictionaries)
        
        self.clipboard = QApplication.clipboard()

        self.ui.lineEdit.returnPressed.connect(self.updateUi)

        self.ui.comboBox.activated.connect(self.on_combo_change)
        
        self.ui.webView.settings().setUserStyleSheetUrl(
                                               QUrl.fromLocalFile(':/lexi.css'))

        self.ui.listView.clicked.connect(self.on_row_clicked)

        self.clipboard.dataChanged.connect(self.get_from_clipboard)

        self.manager.finished.connect(self.replyFinished)

        self.loop = QEventLoop()

        self.manager.finished.connect(self.loop.quit)

        self.tagform = []

    def updateUi(self):
        # Check if input text is a word
        if len(unicode(self.ui.lineEdit.text()).split()) <= 1:
            self.formtype = "definition"
            self.fetch("Lexi")
            self.ui.comboBox.clear()
            self.ui.comboBox.addItems(self.tagform)
            self.formtype = "synonyme"
            self.fetch("Syno")
            self.formtype = "antonyme"
            self.fetch("Anto")
        else:
            self.ui.lineEdit.setText("Veuillez entrer UN mot")

    # Copy selected item in list to the clipboard
    def on_row_clicked(self, qmodelindex):
        item = qmodelindex.data(Qt.DisplayRole).toString()
        self.clipboard.setText(item)
#
    def get_from_clipboard(self):
        if self.ui.checkBox.isChecked():
            self.ui.lineEdit.setText(unicode(self.clipboard.text()))
            self.updateUi()
#
    def on_combo_change(self):
        self.formtype = "definition"
        self.fetch("Lexi")


    def fetch(self, dico):
        if dico == "Lexi":
            if not self.ui.comboBox_2.currentIndex():
                url = ("http://www.cnrtl.fr/definition/%s//%s" %
                       (self.ui.lineEdit.text(), self.ui.comboBox.currentIndex()))
            if self.ui.comboBox_2.currentIndex() > 0:
                acad = unicode(self.ui.comboBox_2.currentText())
                acadnum = filter(lambda x: x.isdigit(), acad)
                acadnumf = "academie" + str(acadnum)
                url = ("http://www.cnrtl.fr/definition/%s/%s//%s" %
                       (acadnumf, self.ui.lineEdit.text(), self.ui.comboBox.currentIndex()))
        if dico == "Syno":
            url = ("http://www.cnrtl.fr/synonymie/%s" %
                   (self.ui.lineEdit.text()))
        if dico == "Anto":
            url = ("http://www.cnrtl.fr/antonymie/%s"  %
                   (self.ui.lineEdit.text()))
        self.manager.get(QNetworkRequest(QUrl(url)))
        self.loop.exec_()

    def replyFinished(self, reply):
        data = reply.readAll()
        page = QWebPage()
        page.mainFrame().setContent(data)
        webpage = page.mainFrame().documentElement()
        if self.formtype == "definition":
            result = webpage.findAll("div#contentbox")
            if not self.ui.comboBox_2.currentIndex():
                result_to_remove = webpage.findAll("div.tlf_cvedette")
            if 1 <= self.ui.comboBox_2.currentIndex() <= 3:
                result_to_remove = webpage.findAll("span.tlf_cvedette")
            string_to_remove = result_to_remove.first().toInnerXml()
            final_page = result.first().toInnerXml()
            resultf = final_page.replace(string_to_remove, '')
            self.ui.webView.setHtml(resultf)

            result_box = webpage.findFirst('div#vtoolbar')
            result_test = result_box.findAll("a[href]")
            self.tagform = []
            i = 0
            while i < len(result_test):
                multdef_a = unicode(result_test.at(i).toPlainText())
                # Delete digits in definition title
                multdef_clean = ''.join(c for c in
                    multdef_a if not c.isdigit())
                self.tagform.append(multdef_clean)
                i += 1
        if self.formtype == "synonyme" or "antonyme":
            result = webpage.findAll("td." + self.formtype[:4] + "_format")
            tag = []
            i = 0
            while i < len(result):
                tag.append(result.at(i).firstChild().toPlainText())
                i += 1
            model = ListModel(tag, self)
            if self.formtype == "synonyme":
                self.ui.listView.setModel(model)
            if self.formtype == "antonyme":
                self.ui.listView_2.setModel(model)

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
