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


import argparse
import sys

def main():
    cmd = argparse.ArgumentParser(description="Check for synonyms or antonyms",
        prog='kcnrtl', usage='%(prog)s --help [options] word')

    cmd.add_argument('word', default="", nargs='?',
        help="The word to look for")

    cmd.add_argument('-s', '--synonym', action="store_true",
        help="Display synonyms of any word")

    cmd.add_argument('-a', '--antonym', action="store_true",
        help="Display antonyms of any word")

    args = cmd.parse_args()

    if 'word' in args:
        wordset = args.word

    if len(sys.argv) < 2:
        from kcnrtl.gui.gui import main as _main
        sys.exit(_main())
    else:
        from kcnrtl.fetchparsebs import get_syno_anto
        if args.synonym:
            get_syno_anto(wordset, "synonymie")
        if args.antonym:
            get_syno_anto(wordset, "antonymie")

if __name__ == '__main__':
    main()
