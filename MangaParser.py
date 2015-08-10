from PyQt4 import QtCore, QtGui
from urllib.request import urlopen, urlretrieve
import re
import os

def threadTimer(timeValue): #making information about passed time
	secs = 0
	mins = 0
	hrs = 0
	if timeValue >= 3600:
		hrs = int(timeValue/3600)
		timeValue = timeValue%3600
	if timeValue >= 60:
		mins = int(timeValue/60)
		timeValue = timeValue%60
	secs = timeValue
	if hrs >= 10:
		hrs = str(hrs) + ":"
	elif hrs:
		hrs = "0"+str(hrs)+":"
	elif not hrs:
		hrs = "00:"
	if mins >= 10:
		mins = str(mins)+":"
	elif mins:
		mins = "0"+str(mins)+":"
	elif not mins:
		mins = "00:"
	if secs >= 10:
		secs = str(secs)
	elif secs:
		secs = "0"+str(secs)
	elif not secs:
		secs = "00"
	return hrs+mins+secs

class DownloadingThread(QtCore.QThread):
	def __init__(self, parent=None):
		QtCore.QThread.__init__(self, parent)
		self.timer = Timer()

		self.connect(self.timer, QtCore.SIGNAL("mysignal(QString)"), self.sendTimeValue)

	def run(self): #downloading thread
		self.emit(QtCore.SIGNAL("buttonLock(bool)"), True)
		
		#opening temporary files and reading information
		titleToDownload = ""
		totalChapters = 1
		infFile = open("tmp\\inf", "r")
		for line in infFile:
			try:
				int(line)
			except:
				titleToDownload = line
			else:
				totalChapters = str(line)

		if not os.path.exists("library\\"+titleToDownload):
			os.mkdir("library\\"+titleToDownload)
    
    #analyzing inforamtion from tmp files and retrieving files
		fileList = []
		tmp_fileList = []
		chNums = []
		imagesNumber = 0
		f = open("tmp\\images", "r")
		for line in f:
			try:
				int(line)
			except:
				tmp_fileList.append(line)
				imagesNumber += 1
			else:
				chNums.append(int(line))
				fileList.append(tmp_fileList)
				for i in range(0, len(tmp_fileList)):
					tmp_fileList.pop(0)
		ch = 0
		for chapter in fileList:
			self.timer.start()
			QtGui.qApp.processEvents()
			counter = 0
			ch += 1
			path = "library\\"+titleToDownload+"\\ch"+str(ch)
			if not os.path.exists(path):
				os.mkdir(path)
			for image in chapter:
				QtGui.qApp.processEvents()
				counter += 1
				if not os.path.isfile(path+"\\"+str(counter)+".jpg"):
					urlretrieve(image, path+"\\"+str(counter)+".jpg")
					self.emit(QtCore.SIGNAL("logAdd(QString)"), path+"\\"+str(counter)+".jpg - complete")
				else:
					continue
				progress = (counter/imagesNumber)*100
				self.emit(QtCore.SIGNAL("progressIncrement(int)"), progress)
			self.emit(QtCore.SIGNAL("logAdd(QString)"), "<p style='color: green'>Download complete!<p>")
			self.timer.running = False
			self.emit(QtCore.SIGNAL("buttonLock(bool)"), False)

	def sendTimeValue(self, timeValue):
		self.emit(QtCore.SIGNAL("mysignal(QString)"), timeValue)

class Timer(QtCore.QThread): #thread of the timer. actually i don't give an idea why i made it to another thread
	def __init__(self, parent=None):
		QtCore.QThread.__init__(self, parent)
		self.running = False
		self.count = -1
		self.time_passed = 0
	def run(self):
		self.running = True
		while self.running:
			self.count += 1
			self.time_passed = threadTimer(self.count)
			self.emit(QtCore.SIGNAL("mysignal(QString)"), "Времени прошло: %s" % self.time_passed)
			self.sleep(1)

class mainWindow(QtGui.QWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.timeLabel = QtGui.QLabel("Прошло времени: --:--:--")

		self.downloading = DownloadingThread()

		self.setWindowIcon(QtGui.QIcon("favico.ico"))
		self.setWindowTitle("MangaParser")

		self.titleName = QtGui.QLineEdit()
		self.chapterNum = QtGui.QLineEdit()

		self.button = QtGui.QPushButton("Download")

		self.downloadLog = QtGui.QTextEdit()
		self.downloadLog.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

		self.progress = QtGui.QProgressBar()

		self.form = QtGui.QFormLayout()
		self.form.addRow("Введите название манги:", self.titleName)
		self.form.addRow("Введите количество глав:", self.chapterNum)
		self.form.addRow(self.button)
		self.form.addRow(self.timeLabel)
		self.form.addRow(self.downloadLog)
		self.form.addRow(self.progress)
		self.setLayout(self.form)

		self.resize(570, 325)

		self.connect(self.button, QtCore.SIGNAL("clicked()"), self.checkUrl)
		self.connect(self.downloading, QtCore.SIGNAL("mysignal(QString)"), self.timeIncrement)
		self.connect(self.downloading, QtCore.SIGNAL("logAdd(QString)"), self.downloadLogAppend)
		self.connect(self.downloading, QtCore.SIGNAL("progressIncrement(int)"), self.changeStatusBar)
		self.connect(self.downloading, QtCore.SIGNAL("buttonLock(bool)"), self.buttonLocker)

	def checkUrl(self): #checking url for existing
		title = self.titleName.text()
		urlPath = self.urlMaking(title)
		try:
			urlopen(urlPath)
		except:
			self.downloadLog.append("""
				<p style="color: red">Error 404. Try again(%s)</p>
				""" % urlPath)
		else:
			self.download()

	def download(self):
		title = self.titleName.text()
		chapterNum = int(self.chapterNum.text())
		self.downloadProcess(title, chapterNum)

	def tmpFileMake(self, urlPath, chaptersNum): #making temporary files
		QtGui.qApp.processEvents()

		if not os.path.exists("tmp"):
			os.mkdir("tmp")

		if not os.path.exists("library"):
			os.mkdir("library")

		f = open("tmp\\images", "w")
		f.close()
		f = open("tmp\\page", "w")
		f.close()
		f = open("tmp\\inf", "w")
		f.close

		urlPath_tmp = urlPath.split("/")
		titleName = urlPath_tmp[3]

		for ch in range(1, chaptersNum+1):
			QtGui.qApp.processEvents()
			urlPath = "http://adultmanga.ru/"+titleName+"/vol1/"+str(ch)+"?mature=1"
			page = urlopen(urlPath)
			page = page.read()
			f_page = open("tmp\\page", "w", encoding="utf-8-sig")
			page = str(page)
			f_page.write(page)
			f_page.close()

			contents = ""
			f_page = open("tmp\\page", "r", encoding="utf-8-sig")
			contents = f_page.read()
			start_s = contents.find("var pictures")
			end_s = contents.find(";", start_s)
			contents = contents[start_s:end_s]
			images = []
			p = re.compile('"(.*?)"')
			images = p.findall(contents)
			f_page.close()

			imageList = open("tmp\\images", "a")
			imageList.write("%d\n" % ch)
			imageList.write("\n".join(images))
			imageList.write("\n")

	def urlMaking(self, title):
		title = title.lower()
		title = title.split()
		title = "_".join(title)
		return "http://adultmanga.ru/"+title+"/vol1/1?mature=1"

	def downloadProcess(self, titleName, ch_num):
		path = "http://adultmanga.ru/"+titleName+"/vol1/1?mature=1"
		urlPath = self.urlMaking(titleName)
		self.tmpFileMake(urlPath, ch_num)
		f = open("tmp\\inf", "a")
		f.write(str(ch_num))
		f.write("\n")
		f.write(titleName)
		f.close()
		self.downloading.start()
		self.logging()

	def logging(self):
		log = open("last run.log", "w")
		lastRun = self.downloadLog.toPlainText()
		log.write(lastRun)
		log.close()

	def timeIncrement(self, s):
		self.timeLabel.setText(s)

	def stopTimer(self):
		self.timer.running = False

	def downloadLogAppend(self, s):
		self.downloadLog.append(s)

	def changeStatusBar(self, num):
		self.progress.setValue(num)

	def buttonLocker(self, locker):
		self.button.setDisabled(locker)

if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	window = mainWindow()
	window.show()
	sys.exit(app.exec_())
