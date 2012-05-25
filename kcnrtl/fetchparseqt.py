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


from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt4.QtWebKit import QWebPage
from PyQt4.QtCore import QEventLoop, QUrl


class FetchParse:
    def __init__(self, word, dico, combo1_index, combo2_index, combo2_text, wordclass):
        self.word = word
        self.dico = dico
        self.combo1_index = combo1_index
        self.combo2_index = combo2_index
        self.combo2_text = combo2_text
        self.wordclass = wordclass
        self.manager = QNetworkAccessManager()
        self.manager.finished.connect(self.replyFinished)
        self.loop = QEventLoop()
        self.manager.finished.connect(self.loop.quit)
        self._reply = ""

    def _get_reply(self):
        self.fetch(self.dico)
        return self._reply

    reply = property(_get_reply)

    def fetch(self, dico):
        if dico == "Lexi":
            if not self.combo2_index:
                url = ("http://www.cnrtl.fr/definition/%s//%s" %
                       (self.word, self.combo1_index))
            if self.combo2_index > 0:
                acad = unicode(self.combo2_text)
                acadnum = filter(lambda x: x.isdigit(), acad)
                acadnumf = "academie" + str(acadnum)
                url = ("http://www.cnrtl.fr/definition/%s/%s//%s" %
                       (acadnumf, self.word, self.combo1_index))
        if dico == "Syno":
            url = ("http://www.cnrtl.fr/synonymie/%s" %
                   (self.word))
        if dico == "Anto":
            url = ("http://www.cnrtl.fr/antonymie/%s"  %
                   (self.word))
        self.manager.get(QNetworkRequest(QUrl(url)))
        self.loop.exec_()

    def replyFinished(self, datareply):
        data = datareply.readAll()
        page = QWebPage()
        page.mainFrame().setContent(data)
        webpage = page.mainFrame().documentElement()
        if self.wordclass == "definition":
            result = webpage.findAll("div#contentbox")
            a = ""
            if not self.combo2_index:
                a = "div.tlf_cvedette"
            if 1 <= self.combo2_index <= 3:
                a = "span.tlf_cvedette"
            result_to_remove = webpage.findAll(a)
            string_to_remove = result_to_remove.first().toInnerXml()
            final_page = result.first().toInnerXml()
            resultf = final_page.replace(string_to_remove, '')

            result_box = webpage.findFirst('div#vtoolbar')
            result_test = result_box.findAll("a[href]")
            self.formtype = []
            i = 0
            while i < len(result_test):
                multdef_a = unicode(result_test.at(i).toPlainText())
                # Delete digits in definition title
                multdef_clean = ''.join(c for c in
                    multdef_a if not c.isdigit())
                self.formtype.append(multdef_clean)
                i += 1
            self._reply = resultf, self.formtype
        if self.wordclass == "synonyme" or self.wordclass == "antonyme":
            self._reply = []
            result = webpage.findAll("td." + self.wordclass[:4] + "_format")
            tag = []
            i = 0
            while i < len(result):
                tag.append(result.at(i).firstChild().toPlainText())
                i += 1
            self._reply = tag

