#!/usr/bin/env python
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

#TODO encripting file /opt/cprocsp/bin/amd64/cryptcp -encr -f «имя_сертификата.cer» nonencrypted encrypted

import rosa_crypto_tool_ui
import rosa_crypto_tool_main
import gettext
import sys
import os.path

def main():
	gettext.install('rosa-crypto-tool', unicode=True)
	
	app = rosa_crypto_tool_ui.QApplication(sys.argv)
	app_ui = rosa_crypto_tool_ui.MainWindow()
	app_core = rosa_crypto_tool_main.RosaApp(app_ui)
	sys.exit(app.exec_())

if __name__ == '__main__':
	
	main()
