# -*- coding: utf-8 -*-
"""
Created on Fri May 25 16:05:36 2018

@author: Administrator
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import regexTesterUi

class TestDialog(QDialog,regexTesterUi.Ui_Dialog):
    def __init__(self,parent=None):
        super(TestDialog,self).__init__(parent)
        self.setupUi(self)
       
if __name__ == '__main__':
    app=QApplication(sys.argv)
    dialog=TestDialog()
    dialog.show()
    app.exec_()