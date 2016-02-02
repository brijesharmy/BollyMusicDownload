import requests
import re
from bs4 import BeautifulSoup
import os

res = requests.get('http://djmaza.info/')

res.raise_for_status()

home = BeautifulSoup(res.text, 'html5lib')

songs = home.select('#fasy4 > a')[:10]

if not os.path.isdir('./Downloads'):
	os.system('mkdir Downloads')



for song in songs:
	songpg = requests.get('http://djmaza.info/' + song.attrs['href'])
	songpg.raise_for_status()
	songpg = BeautifulSoup(songpg.text, 'html5lib')
	if song.attrs['href'].endswith('Singles.html'):
		songpg = songpg.select('#border_both173 a')
	else:
		songpg = songpg.select('#border_both342 a')
	if songpg:
		songdwnld = requests.get(songpg[0].attrs['href'])
		songdwnld.raise_for_status()
		if song.attrs['href'].endswith('Singles.html'):
			filename = '%s.mp3' % songpg[0].get_text().strip()
		else:
			filename = '%s.zip' % songpg[0].get_text().strip()
		print filename
		
		filename = re.sub('\s+', ' ', filename)
		unwantedchars = ['/',':','*','"','<','>','|','?']
		for ch in unwantedchars:
			if ch in filename:
				filename = filename.replace(ch,' ')
		
		fullfilepath = os.path.join(os.getcwd(),'Downloads', filename)
		songfile = open(fullfilepath, 'wb')
		for chunk in songdwnld.iter_content(100000):
			songfile.write(chunk)
		songfile.close()
