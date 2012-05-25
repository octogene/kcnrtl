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

import httplib2
from bs4 import BeautifulSoup

def getSynoAnto(text, form):
    conn = httplib2.Http(".cache")
    htmlSource = conn.request("http://www.cnrtl.fr/%s/%s" %
                                  (form, text), "GET")
    soup = BeautifulSoup(htmlSource[1], "lxml")
    tagy = soup.find_all('td', "%s_format" % (form[:4]))
    i = 0
    while i < len(tagy):
        tag_a = tagy[i]
        i += 1
        print tag_a.text


