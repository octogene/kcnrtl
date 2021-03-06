======
KCnrtl
======

:Author: Bogdan Cordier <bcord@hadaly.fr>
:Date: 2012-26-05
:Copyright: GPLv3
:Version: 0.4rc2


Description
===========

KCnrtl is a simple Qt graphical client to access the CNRTL french linguistic resources.

Features:
---------

    *Check the synomyms, antonyms (CLI & GUI), definitions (GUI only) of any given french word

    *Dictionaries available for now:
        -TLFi (Trésor de la Langue Française informatisé)
        -Dictionnaire de l'Académie Française 9th, 8th & 4th Edition

    *Clipboard mode (GUI only) :
      With the "Clipboard mode" you can easily check for a synonym/antonym and replace it in your text.
      To do so, just check the "Clipboard mode" checkbox, copy in the clipboard any word, KCnrtl will do
      an automatic request to the CNRTL website and you can easily copy any synonym or antonym by
      just clicking on them in the result list.
      Now you just have to paste it back in you text !

Planned features:
-----------------

    *access to other dictionaries offered by the CNRTL (Dictionnaire du Moyen Français, etc)

Installation
============

Decompress the archive.
In console go to the destination directory:

::

python setup.py install

Or you can directly launch the program by running kcnrtl.py in the destination directory

Requirements
============

*Python: 2.7
*PyQt4: >= 4.6
*beautifulsoup4
*httplib2
*lxml

