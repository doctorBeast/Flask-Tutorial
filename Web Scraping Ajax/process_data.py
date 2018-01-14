import requests
import sys
from PyQt5.QtWidgets import QApplication 
from PyQt5.QtCore import QUrl 
from PyQt5.QtWebEngineWidgets import QWebEnginePage,QWebEngineView
from bs4 import BeautifulSoup
import urllib.request
from dateutil import parser
from datetime import datetime


# class Client(QWebPage):

# 	def __init__(self,url):
# 		self.app = QApplication(sys.argv)
# 		QWebPage.__init__(self)
# 		self.loadFinished.connect(self.on_page_load)
# 		self.mainFrame().load(QUrl(url))

# 	def on_page_load(self):
		# self.app.quit()

class Page(QWebEnginePage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print('Load finished')

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()


def func(stn_name = None , start_time = None , end_time = None):
	url = 'https://etrain.info/in?PAGE=howto-arrivaldeparture#!STATION=' + stn_name
	source = Page(url)

	# app = QApplication(sys.argv)
	# browser = QWebEngineView()
	# browser.load(QUrl(url))
	# browser.show()
	# data  =browser.read()
	# app.exec_()

	# client_response = Client(url)
	# source = client_response.mainFrame().toHtml()
	# # print(url)
	# web = urllib.request.urlopen(url)
	# s = web.read()
	# page = requests.get(url)
	# plain_text = page.text
	start_t = datetime.strptime(start_time,"%H:%M")
	print(start_t)
	end_t = datetime.strptime(end_time,"%H:%M")
	print(end_t)
	soup = BeautifulSoup(source.html , "html.parser")
	table = soup.find('table',class_ = 'myTable data nocps nolrborder')
	rows = table.findAll('tr')
	print('DONE')
	html_str = str()
	for row in rows:
		# a = input()
		# if a == 'k':
		# 	print(row.prettify())
		# else:
		# 	break
		flag = 0
		columns = row.findAll('td')
		try:
			arrival_time = datetime.strptime(str(columns[4].string),"%H:%M")
		except ValueError:
			pass
		try:	
			dept_time = datetime.strptime(str(columns[5].string),"%H:%M")
		except ValueError:
			pass

		print(arrival_time)
		if start_t <= end_t:
			try:
				if start_t<= arrival_time <= end_t:
					html_str += str(row)
					flag = 1
				else:
					pass
			except UnboundLocalError:
				pass
			
			try:
				if start_t<= dept_time <= end_t and flag == 0:
					html_str += str(row)
					flag = 1
				else:
					pass
			except UnboundLocalError:
				pass
		else:
			time1 = datetime.strptime("23:59","%H:%M")
			time2 = datetime.strptime("00:00","%H:%M")
			
			try:
				if start_t <= arrival_time<=time1 or time2<=arrival_time <=end_t:
					html_str += str(row)
					flag = 1
				else:
					pass
			except UnboundLocalError:
				pass

			try:
				if (start_t<= dept_time<=time1 or time2<=dept_time <=end_t) and flag == 0:
					html_str += str(row)
					flag = 1
				else:
					pass
			except UnboundLocalError:
				pass

		if flag == 1:
			print(str(columns[0].string))
	
	return html_str