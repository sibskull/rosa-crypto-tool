#!/usr/bin/python

import os
import subprocess
from distutils.core import setup

def get_data():
	""" Return all needed data files """
	
	data = []
	
	for path_dir, list_dir, list_file in os.walk('po/'):
		if list_file != []:
			name_f = list_file[0]
		if path_dir != 'po/':
			po_file = os.path.join(path_dir, name_f)
			mo_file = po_file.replace(".po", '.mo')
			msgfmt = 'msgfmt -c %s -o %s' %(po_file, mo_file)
			subprocess.call(msgfmt, shell = True)
			
			data.append(('share/locale/' + mo_file.split('/')[1] + '/LC_MESSAGES/', [mo_file]))
	
	data += (('share/icons/hicolor/48x48/apps/', ['icon/rosa-crypto-tool.svg']),
		  ('share/doc/rosa-crypto-tool', ['doc/help.pdf']))
	
	return data


setup(name='rosa_crypto_tool',
	  version='0.0.8',
	  description='Program for working with electronic digital signatures.',
	  author='Michl Voznesensky', author_email='m.voznesensky@rosalinux.ru',
	  license = 'BSD',
	  url='http://rosalab.ru',
	  package_dir = {'rosa_crypto_tool': 'src'},
	  packages=['rosa_crypto_tool'],
	  data_files=get_data(),
	  )
