from bs4 import BeautifulSoup
from pyppeteer import launch
from urllib import request
import threading
import requests
import asyncio
import getopt
import queue
import sys
import os 

exitFlag = False

def log(prefix, info):
	print("[" + prefix + "] " + info + ".")

async def getContent(url):
	browser = await launch()
	page = await browser.newPage()
	await page.setJavaScriptEnabled(enabled=True)
	await page.goto(url)

	log("+", "Get content from " + url)
	content = await page.content()
	await browser.close()
	return content	

def DownloadM4aEx(url):
	'''
	Download .M4a from user`s index
	'''
	loop = asyncio.get_event_loop()
	task = asyncio.ensure_future(getContent(url))
	loop.run_until_complete(task)
	soup = BeautifulSoup(task.result(),"html.parser")
	
	links = soup.findAll(name = 'a', attrs = { 'class': 'mod_playlist__cover'})
	for link in links: 
		DownloadM4a(link['href'])
		#threading.Thread(target=DownloadM4a, args=(link['href'],)).start()

def DownloadM4a(url):
	'''
	Download .M4a from share link
	'''
	loop = asyncio.get_event_loop()
	task = asyncio.ensure_future(getContent(url))
	loop.run_until_complete(task)
	soup = BeautifulSoup(task.result(),"html.parser")

	singer = soup.find(name = 'a', attrs = { 'class': 'singer_user__name' }).get_text()
	singer = singer.replace(" ","").replace('\n',"")
	mdir = os.getcwd() 
	path = mdir + "\\Music\\"
	if not os.path.exists(path):
		log("+", "Create a new folder named 'Music'") 
		os.mkdir(path)
	path += singer + "\\"
	if not os.path.exists(path):
		log("+","Create a new folder for singer named " + singer)
		os.mkdir(path)

	name = soup.audio['meta'] + ".m4a"
	uri = soup.audio['src']

	if os.path.exists(path + name):
		log("-", " The music which is " + name + " has existed")
		exit(1)

	log("+","Downloading " + name + " from " + uri + " into " + path)
	music = requests.get(uri)
	with open(path + name, 'wb') as fp:
		fp.write(music.content)

def main(url):
	if url:
		if "personal?uid=" in url:
			try:
				DownloadM4aEx(url)
			except Exception as e:
				log("-", str(e))
		elif "play?s=" in url:
			try:
				DownloadM4a(url)
			except Exception as e:
				log("-", str(e))

if __name__ == '__main__':
	main(input("url:"))