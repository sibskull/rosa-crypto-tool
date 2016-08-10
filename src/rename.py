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

def translit(name_file):
	for i, j in legend.items():
		name_file = name_file.replace(i, j)
	return name_file

legend = {' ':'_', ',':'',
		  'а':'a',
		  'б':'b',
		  'в':'v',
		  'г':'g',
		  'д':'d',
		  'е':'e',
		  'ё':'yo',
		  'ж':'zh',
		  'з':'z',
		  'и':'i',
		  'й':'y',
		  'к':'k',
		  'л':'l',
		  'м':'m',
		  'н':'n',
		  'о':'o',
		  'п':'p',
		  'р':'r',
		  'с':'s',
		  'т':'t',
		  'у':'u',
		  'ф':'f',
		  'х':'h',
		  'ц':'c',
		  'ч':'ch',
		  'ш':'sh',
		  'щ':'shch',
		  'ъ':'y',
		  'ы':'y',
		  'ь':"'",
		  'э':'e',
		  'ю':'yu',
		  'я':'ya',
		  
		  'А':'A',
		  'Б':'B',
		  'В':'V',
		  'Г':'G',
		  'Д':'D',
		  'Е':'E',
		  'Ё':'Yo',
		  'Ж':'Zh',
		  'З':'Z',
		  'И':'I',
		  'Й':'Y',
		  'К':'K',
		  'Л':'L',
		  'М':'M',
		  'Н':'N',
		  'О':'O',
		  'П':'P',
		  'Р':'R',
		  'С':'S',
		  'Т':'T',
		  'У':'U',
		  'Ф':'F',
		  'Х':'H',
		  'Ц':'Ts',
		  'Ч':'Ch',
		  'Ш':'Sh',
		  'Щ':'Shch',
		  'Ъ':'Y',
		  'Ы':'Y',
		  'Ь':"'",
		  'Э':'E',
		  'Ю':'Yu',
		  'Я':'Ya',
		  }
