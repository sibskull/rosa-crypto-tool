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
import os.path
import subprocess
import rename
#rename nedeed for vefify sign
#files with the name Cyrillic characters are not available to take certificate
import re
import datetime
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDesktopWidget

class RosaApp(object):
	""" Logic of the program """
	
	def __init__(self, app_ui):
		self._ui = app_ui #main window
		self._ui_widget = app_ui.main_widget #main widjet (insert to in main window)
		
		self.checkProgramm()
		
		self._ui.open_act.triggered.connect(self.showDialog)
		self._ui.exit_act.triggered.connect(exit)
		
		self._ui.sign_act.triggered.connect(self.createSign)
		self._ui.check_sign_act.triggered.connect(self.verifySignature)
		self._ui.split_file_act.triggered.connect(self.splitFile)
		self._ui.check_comp_act.triggered.connect(self.checkProgramm)
		self._ui.install_cert_act.triggered.connect(self.installCert)
		
		self._ui.help_act.triggered.connect(self.openHelp)
		self._ui.about_act.triggered.connect(self.showAbout)
		
		self._ui_widget.btn_open.clicked.connect(self.showDialog)
		self._ui_widget.btn_sign.clicked.connect(self.createSign)
		self._ui_widget.btn_check_sign.clicked.connect(self.verifySignature)
		self._ui_widget.btn_split_file.clicked.connect(self.splitFile)
	
	def checkProgramm(self):
		""" This checks all the necessary components for the successful operation of the program.
		If something is missing you will see the corresponding message """
		
		sender = self._ui_widget.sender() #slot for registred triggered
		
		if sender == self._ui.check_comp_act:
			map(lambda field: field.setEnabled(True), self._ui.list_off_all)
		
		list_comp = []
		
		if os.path.isdir('/opt/cprocsp/bin/amd64/'):
			self.dir_prog = '/opt/cprocsp/bin/amd64/' #directory CryptoPro
		elif os.path.isdir('/opt/cprocsp/bin/ia32/'):
			self.dir_prog = '/opt/cprocsp/bin/ia32/'
		else: self.dir_prog = '' #next code will automatically be played error
			
		
		try:
			info_cert = subprocess.check_output([self.dir_prog+"csptest", "-keyset", "-enum_cont", "-verifyc", "-fq"]) #console information Rutoken
			info_pcsc = subprocess.call(["pidof", "pcscd"])
			#if info_pcsc == 0 then pcscd running
			if info_pcsc == 0:
				self.name_cert = self.__parseConsole(info_cert, "\\")
				if self.name_cert == "":
					map(lambda field: field.setEnabled(False), self._ui.list_off_sig) #disable components linked to signature
					list_comp.append("token")
			else:
				map(lambda field: field.setEnabled(False), self._ui.list_off_sig)
				list_comp.append("pcsc")
		except OSError:
			map(lambda field: field.setEnabled(False), self._ui.list_off_all)
			list_comp.append("crypto")
		
		if list_comp:
			self.informBox(list_comp)
		else:
			if sender == self._ui.check_comp_act:
				self.informBox(list_comp)
	
	def openHelp(self):
		subprocess.Popen(["okular", "/usr/share/doc/rosa-crypto-tool/help.pdf"]) #Popen allows to start a new process
	
	def showAbout(self):
		current_pos = self._ui.about_program.geometry()
		current_pos.moveCenter(self._ui.geometry().center())
		self._ui.about_program.move(current_pos.topLeft())
		self._ui.about_program.show()
	
	def infoCert(self, where_cert):
		""" Generates information about the certificate.
		When creating a signature file, certificate is taken from Rutoken.
		When verifying a signature - from a file """
		
		if where_cert == "token":
			status_cert = subprocess.check_output([self.dir_prog+"certmgr", "-list", "-cont", self.name_cert])
		elif where_cert == "file":
			status_cert = subprocess.check_output([self.dir_prog+"certmgr", "-list", "-file", self._ui_widget.file_edit.text()])
		
		self.name_subj = self.__parseConsole(status_cert, "Subject") #need to sign the files (finding certificate)
		row_valid_cert = self.__parseConsole(status_cert, "Not valid after") #need to check valid certificate
		self.gost = self.__parseConsole(status_cert, "Signature Algorithm")
		
		valid_cert = re.findall('[0-9]{2,4}',row_valid_cert) #take data
		valid_cert = map(lambda x: int(x), valid_cert) #chage type data
		self.date_valid_cert = datetime.datetime(valid_cert[2], valid_cert[1], valid_cert[0], valid_cert[3], valid_cert[4], valid_cert[5])
		
		self.out_status_cert = _("Information about the certificate:\n") +\
							_("- Issuer: ") + self.__parseConsole(status_cert, "Issuer") + "\n" +\
							_("- Subject: ") + self.name_subj + "\n" +\
							_("- Serial: ") + self.__parseConsole(status_cert, "Serial") + "\n" +\
							_("- Signature Algorithm: ") + self.gost + "\n" +\
							_("- PublicKey Algorithm: ") + self.__parseConsole(status_cert, "PublicKey Algorithm") + "\n" +\
							_("- Valid from ") + self.__parseConsole(status_cert, "Not valid before") + _(" to ") + row_valid_cert
	
	def showDialog(self):
		""" Open file """
		
		self.path_name = QFileDialog.getOpenFileName(self._ui, _("Choose file"), os.path.expanduser("~"))[0]
		
		if self.path_name:
			self.__parseDir(self.path_name)
			self._ui_widget.file_edit.setText(self.file_name)
	
	def verifySignature(self):
		""" Verify file with the extension .sig """
		
		try:
			if self._ui_widget.file_edit.text():
				os.chdir(self.currently_dir)
				#If you do not change directory to the directory
				#of the current file, the certificate file is not found
				
				yes = subprocess.Popen(["yes"], stdout=subprocess.PIPE)
				status_check_sign = subprocess.check_output([self.dir_prog+"cryptcp", "-verify", self.path_name.encode('utf-8'), "-f", self.file_name], stdin=yes.stdout)
				if "Signature's verified" in status_check_sign:
					out_status_check_sign = _("Signature's verified")
				
				self._ui_widget.icon_status_oper.setPixmap(self._ui_widget.icon_success)
				self._ui_widget.mes_status_oper.setText(out_status_check_sign)
				
				self.infoCert("file")
				self._ui_widget.result.setText(out_status_check_sign + "\n\n" + self.out_status_cert + self.__validDate(self.date_valid_cert, self.gost))
			else:
				out_status_check_sign = _("Please select the file to verify sign")
				
				self._ui_widget.icon_status_oper.setPixmap(self._ui_widget.icon_atten)
				self._ui_widget.mes_status_oper.setText(out_status_check_sign)
				
				self._ui_widget.result.setText(out_status_check_sign)
		except subprocess.CalledProcessError:
			if self._ui_widget.file_edit.text() != "":
				out_status_check_sign = _("This file is not a signature")
				
				self._ui_widget.icon_status_oper.setPixmap(self._ui_widget.icon_failed)
				self._ui_widget.mes_status_oper.setText(out_status_check_sign)
				
				self._ui_widget.result.setText(out_status_check_sign)
	
	def splitFile(self):
		""" Retrieves the file from the container *.sig """
		
		try:
			if self._ui_widget.file_edit.text():
				os.chdir(self.currently_dir)
				#If you do not change directory to the directory
				#of the current file, the certificate file is not found
				if '.sig' in self.file_name:
					new_name = self.file_name[:self.file_name.rindex(".")] #separate extention .sig
				else:
					new_name = "new_" + self.file_name
				
				yes = subprocess.Popen(["yes"], stdout=subprocess.PIPE)
				status_check_sign = subprocess.check_output([self.dir_prog+"cryptcp", "-verify", self.path_name.encode('utf-8'), new_name, "-f", self.file_name], stdin=yes.stdout)
				if "Signature's verified" in status_check_sign:
					out_status_check_sign = _("The file is separated")
				
				self._ui_widget.icon_status_oper.setPixmap(self._ui_widget.icon_success)
				self._ui_widget.mes_status_oper.setText(out_status_check_sign)
				
				self.infoCert("file")
				self._ui_widget.result.setText(out_status_check_sign + "\n\n" + self.out_status_cert)
			else:
				out_status_check_sign = _("Please select the file sign to separated")
				
				self._ui_widget.icon_status_oper.setPixmap(self._ui_widget.icon_atten)
				self._ui_widget.mes_status_oper.setText(out_status_check_sign)
				
				self._ui_widget.result.setText(out_status_check_sign)
		except subprocess.CalledProcessError:
			if self._ui_widget.file_edit.text() != "":
				out_status_check_sign = _("This file is not a signature")
				
				self._ui_widget.icon_status_oper.setPixmap(self._ui_widget.icon_failed)
				self._ui_widget.mes_status_oper.setText(out_status_check_sign)
				
				self._ui_widget.result.setText(out_status_check_sign)
	
	def createSign(self):
		""" Create sign for file with the extension .sig """
		
		try:
			if self._ui_widget.file_edit.text():
				self.infoCert("token")
				
				yes = subprocess.Popen(["yes"], stdout=subprocess.PIPE)
				status_sig = subprocess.check_output([self.dir_prog+"cryptcp", "-dir", self.currently_dir, "-sign", "-dn", self.name_subj, "-der", self.path_name, self.currently_dir + rename.translit(self.file_name) + ".sig"], stdin=yes.stdout)
				if "Signed message is created" in status_sig:
					out_status_sig = _("Signed message is created")
				
				self._ui_widget.icon_status_oper.setPixmap(self._ui_widget.icon_success)
				self._ui_widget.mes_status_oper.setText(out_status_sig)
				
				self._ui_widget.result.setText(out_status_sig + "\n\n" + self.out_status_cert + self.__validDate(self.date_valid_cert, self.gost))
			else:
				out_status_sig = _("Please select the file to sign")
				
				self._ui_widget.icon_status_oper.setPixmap(self._ui_widget.icon_atten)
				self._ui_widget.mes_status_oper.setText(out_status_sig)
				
				self._ui_widget.result.setText(out_status_sig)
		except subprocess.CalledProcessError:
			out_status_sig = _("Certificate you want to sign the document is not installed.\nPlease click on the button to install the certificate and try again")
			
			self._ui_widget.icon_status_oper.setPixmap(self._ui_widget.icon_failed)
			self._ui_widget.mes_status_oper.setText(out_status_sig)
			
			self._ui_widget.result.setText(out_status_sig)
	
	def installCert(self):
		""" Installing certificate from Rutoken """
		
		result = subprocess.call([self.dir_prog+"certmgr", "-inst", "-cont", self.name_cert, "-store", "uMy"])
		if result == 0:
			out_status_install_cert = _("The certificate was installed successfully")
			
			self._ui_widget.icon_status_oper.setPixmap(self._ui_widget.icon_success)
			self._ui_widget.mes_status_oper.setText(out_status_install_cert)
			
			self._ui_widget.result.setText(out_status_install_cert)
		else:
			out_status_install_cert = _("The installation failed.\nPlease check for the token in the computer and try again")
			
			self._ui_widget.icon_status_oper.setPixmap(self._ui_widget.icon_failed)
			self._ui_widget.mes_status_oper.setText(out_status_install_cert)
			
			self._ui_widget.result.setText(out_status_install_cert)
	
	def __parseConsole(self, cert, field):
		""" Separate output from the console by selecting the rows
		and pulling from it the necessary information """
		
		entry = cert.find(field) #fisrt entry field
		end_row = cert[entry:].find("\n")
		row = cert[entry:(entry + end_row)]
		if field == "Issuer" or field == "Subject":
			#This parsing basically uses to catch name Subject
			new_entry = row.find("CN=")+3
			end_new_row = row[new_entry:].find(",")
			if end_new_row >= 0:
				key_word = row[new_entry:(new_entry + end_new_row)]
			else:
				key_word = row[new_entry:]
			
		elif field == "\\":
			key_word = row
		else:
			key_word = row[row.find(": ")+2:]
		return key_word.decode('utf-8')
	
	def __parseDir(self, path):
		""" Share the current directory of the file and file name """
		
		self.file_name = path[path.rindex("/")+1:].encode('utf-8') #search last entry "/" and make the cut
		self.currently_dir = path[:path.rindex("/")+1].encode('utf-8') #search last entry "/" and make the cut
	
	def __validDate(self, date, gost):
		""" Check valid cert """
		message = ""
		
		current_datetime = datetime.datetime.utcnow()
		if date < current_datetime:
			message += _(" - no longer valid\n")
		if '2001' in gost:
			message += _(" - using outdated signature scheme %s valid until 31 December 2018\n") %gost
		
		if message:
			self.informBox(message, True)
			return _("\n\nWARNING: This certificate:\n") + message
	
	def informBox(self, list_comp, about_cert = None):
		""" Create MessageBox """
		
		if about_cert is None:
			out_list = ""
			if list_comp:
				for comp in list_comp:
					if comp == 'token':
						out_list += _(" - Token is not installed in the computer\n")
					elif comp == 'crypto':
						out_list += _(" - CryptoPro is not installed in the computer\n")
					elif comp == 'pcsc':
						out_list += _(" - PC/SC Smart Card Daemon is not running\n")
				
				QMessageBox.warning(self._ui, _("Warning"), _("Discovered the following:\n\n") + out_list, QMessageBox.Ok)
			else:
				QMessageBox.information(self._ui, _("Information"), _("All the necessary components installed and working"), QMessageBox.Ok)
		
		else:
			QMessageBox.warning(self._ui, _("Warning"), _("This certificate:\n\n") + list_comp, QMessageBox.Ok)

if __name__ == '__main__':
	
	print "You run the part program rosa crypto tool, please launch the main file"
