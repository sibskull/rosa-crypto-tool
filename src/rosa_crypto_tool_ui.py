# -*- coding: utf-8 -*-
################################################################################
#
# ROSA Crypto
#
# Copyright (c) 2016, LLC "NTC IT ROSA"
# License: BSD
# Authors:
#     Michl Voznesensky <m.voznesensky@rosalinux.ru>
#
# This file is a part of ROSA Crypto
#
# All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#  
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following disclaimer
#    in the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of the LLC "STC IT ROSA" nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#  
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
################################################################################

import sys
import os
from PyQt5.QtWidgets import QApplication, qApp, QMainWindow, QWidget, QGridLayout, QPushButton, QLabel, QLineEdit, QDesktopWidget, QMessageBox, QShortcut, QTextEdit, QFileDialog, QAction, QSizePolicy, QHBoxLayout, QVBoxLayout, QFrame
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QKeySequence, QPixmap, QFont

max_width = 1024
min_height = 260
max_height = 600

class MainWindow(QMainWindow):
	""" Main window """
	
	def __init__(self):
		""" Create main widget (window) """
		
		super(MainWindow, self).__init__()
		
		self.setFixedHeight(min_height)
		self.setMaximumWidth(max_width)
		
		#MeuBar
		menubar = self.menuBar()
		appFile = menubar.addMenu(_('&File'))
		appTools = menubar.addMenu(_('&Tools'))
		appHelp = menubar.addMenu(_('&Help'))
		
		#action
		self.open_act = QAction(QIcon.fromTheme('fileopen'), _("&Choose File"), self)
		self.open_act.setShortcut(QKeySequence.Open)
		self.open_act.setToolTip(_("Choose file for sign or verify signature"))
		self.exit_act = QAction(QIcon.fromTheme('exit.svg'), _("&Exit"), self)
		self.exit_act.setShortcut(QKeySequence.Quit)
		
		self.sign_act = QAction(QIcon.fromTheme('stock_edit.svg'), _("&Sign file"), self)
		self.sign_act.setToolTip(_("Sign the selected file"))
		self.check_sign_act = QAction(QIcon.fromTheme('edit-find-replace.svg'), _("&Check signature"), self)
		self.check_sign_act.setToolTip(_("Verify a signed file"))
		self.split_file_act = QAction(QIcon.fromTheme('down'), _("Split file"), self)
		self.split_file_act.setToolTip(_("Separates the file from your signature"))
		self.check_comp_act = QAction(_("Check component program"), self)
		self.install_cert_act = QAction(QIcon.fromTheme('system-upgrade.svg'),_("Install certificate"), self)
		
		self.help_act = QAction(QIcon.fromTheme('help-contents'), _("&Help"), self)
		self.help_act.setShortcut(QKeySequence.HelpContents)
		self.about_act = QAction(QIcon.fromTheme('help-about'), _("&About ROSA Crypto Tool"), self)
		
		#add action
		appFile.addAction(self.open_act)
		appFile.addSeparator()
		appFile.addAction(self.exit_act)
		
		appTools.addAction(self.sign_act)
		appTools.addAction(self.check_sign_act)
		appTools.addAction(self.split_file_act)
		appTools.addSeparator()
		appTools.addAction(self.check_comp_act)
		appTools.addSeparator()
		appTools.addAction(self.install_cert_act)
		
		appHelp.addAction(self.help_act)
		appHelp.addAction(self.about_act)
		
		self.about_program = AboutWidget()
		self.main_widget = MainWidget(self)
		self.setCentralWidget(self.main_widget)
		
		self.main_widget.btn_details.clicked.connect(self.showMore)
		
		self.list_off_sig = [self.main_widget.btn_sign, self.install_cert_act, self.sign_act]
		self.list_off_all = [self.open_act, self.sign_act, self.check_sign_act, self.split_file_act,\
							self.main_widget.btn_open, self.main_widget.btn_sign, self.main_widget.btn_check_sign, self.main_widget.btn_split_file,\
							self.main_widget.file_edit, self.install_cert_act]
		
		self.resize(640, min_height) #widht and hight window
		
		self.setWindowTitle(_("ROSA Crypto Tool"))
		self.setWindowIcon(QIcon.fromTheme('rosa-crypto-tool.svg'))
		self.show()
	
	def showMore(self):
		if self.main_widget.result.isVisible():
			self.main_widget.btn_details.setText(_("Show"))
			self.main_widget.result.setVisible(False)
			self.setFixedHeight(min_height)
		else:
			self.main_widget.btn_details.setText(_("Hide"))
			self.main_widget.result.setVisible(True)
			self.setFixedHeight(max_height)
	
	def resizeEvent(self, e):
		if not self.isMaximized():
			if self.main_widget.result.isVisible():
				self.resize(QSize(self.width(), min_height))
			else:
				self.resize(QSize(self.width(), max_height))

class MainWidget(QWidget):
	""" Main widgets applicatioin """
	
	def __init__(self, parent = None):
		super(MainWidget, self).__init__(parent)
		
		self.parent = parent
		
		#Labels
		file = QLabel(_("File:"))
		status_oper = QLabel(_("Status operation:"))
		details = QLabel(_("Details:"))
		self.mes_status_oper = QLabel()
		self.icon_status_oper = QLabel()
		
		self.icon_success = QIcon.fromTheme('package-reinstall').pixmap(22,22)
		self.icon_atten = QIcon.fromTheme('package-broken').pixmap(22,22)
		self.icon_failed = QIcon.fromTheme('package-purge').pixmap(22,22)
		
		#Fields Edit
		self.file_edit = QLineEdit(readOnly = True)
		self.result = QTextEdit(readOnly = True)
		self.result.setVisible(False)
		
		#Buttons
		self.btn_open = QPushButton(self.parent.open_act.icon(), _("Choose"))
		self.btn_open.setToolTip(self.parent.open_act.toolTip())
		self.btn_sign = QPushButton(self.parent.sign_act.icon(), self.parent.sign_act.text())
		self.btn_sign.setToolTip(self.parent.sign_act.toolTip())
		self.btn_check_sign = QPushButton(self.parent.check_sign_act.icon(), self.parent.check_sign_act.text())
		self.btn_check_sign.setToolTip(self.parent.check_sign_act.toolTip())
		self.btn_split_file = QPushButton(self.parent.split_file_act.icon(), self.parent.split_file_act.text())
		self.btn_split_file.setToolTip(self.parent.split_file_act.toolTip())
		self.btn_details = QPushButton(_("Show"))
		self.btn_details.setToolTip(_("Show or hide more information"))
		
		#Grid
		grid = QGridLayout()
		grid.setSpacing(5)
		
		grid.addWidget(file, 0, 0)
		grid.addWidget(self.file_edit, 0, 1)
		grid.addWidget(self.btn_open, 0, 2)
		
		grid.addWidget(self.btn_sign, 1, 2)
		frame_check_sig = QFrame(self)
		frame_check_sig.setFrameShape(QFrame.StyledPanel)
		vbox_check_sig = QVBoxLayout()
		vbox_check_sig.addWidget(self.btn_check_sign)
		vbox_check_sig.addWidget(self.btn_split_file)
		frame_check_sig.setLayout(vbox_check_sig)
		grid.addWidget(frame_check_sig, 2, 2)
		
		grid.addWidget(status_oper, 3, 0)
		hbox_status = QHBoxLayout()
		hbox_status.addWidget(self.icon_status_oper)
		hbox_status.addWidget(self.mes_status_oper)
		hbox_status.addStretch(1)
		grid.addLayout(hbox_status, 3, 1)
		grid.setRowMinimumHeight(3, 22)
		
		grid.addWidget(details, 4, 0)
		grid.addWidget(self.result, 4, 1, 4, 1)
		grid.addWidget(self.btn_details, 4, 2)
		
		grid.setRowStretch(5,1)
		
		self.setLayout(grid)

class AboutWidget(QWidget):
	""" Widget about program """
	
	def __init__(self, parent = None):
		super (AboutWidget, self).__init__(parent)
		
		self.parent = parent
		
		rosa_logo = QIcon.fromTheme('rosa-crypto-tool.svg').pixmap(48,48)
		logoLabel = QLabel()
		logoLabel.setPixmap(rosa_logo)
		
		messages = QLabel()
		messages.setText(_("ROSA Crypto Tool - program for working with electronic digital signature\n\n"
						"Authors: Michl Voznesensky\n" +\
						"Version: alpha\n" +\
						"License: BSD\n" +\
						"Copyright (c) 2016, LLC \"NTC IT ROSA\""))
		
		grid = QGridLayout()
		grid.setSpacing(5)
		grid.addWidget(logoLabel, 0, 0, Qt.AlignCenter)
		grid.addWidget(messages, 1, 0, Qt.AlignCenter)
		
		self.setLayout(grid)
		
		self.resize(250, 150) #widht and hight window
		
		self.setWindowTitle(_("About ROSA Crypto Tool"))
		self.setWindowIcon(QIcon.fromTheme('help-about'))


if __name__ == '__main__':
	
	print "You run the part program rosa crypto tool, please launch the main file"