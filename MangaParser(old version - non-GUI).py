from urllib.request import urlopen, urlretrieve
import re, os

def fetch_files(file_list, ch, titleToDownload):
	path = titleToDownload+"\ch"+str(ch)
	print(path)
	if not os.path.exists(path):
			os.mkdir(path)
	for i in range(0, len(file_list)):
		if not os.path.isfile(path+"\\"+str(i+1)+".jpg"):
			urlretrieve(file_list[i], path+"\\"+str(i+1)+".jpg")
		print(file_list[i]+" - complete - " + path + "\\"+str(i+1)+".jpg")
	print("Download complete!")

def tmpFileMake(urlPath, currentChapterNumber):
	tmp = open("tmp.txt", "w", encoding="utf-8-sig")
	tmp.write("")
	tmp.close()
	urlPath_tmp = urlPath.split("/")
	titleName = urlPath_tmp[3]
	urlPath = "http://adultmanga.ru/"+titleName+"/vol1/"+str(currentChapterNumber)+"?mature=1"
	page = urlopen(urlPath)
	page = page.read()
	f_page = open("tmp.txt", "w", encoding="utf-8-sig")
	page = str(page)
	f_page.write(page)
	f_page.close()

def urlMaking(title):
	title = title.lower()
	title = title.split()
	title = "_".join(title)
	return "http://adultmanga.ru/"+title+"/vol1/1?mature=1"

def downloadProcess(title_name, ch_num):
	path = "http://adultmanga.ru/"+title_name+"/vol1/1?mature=1"
	res = 0
	while not res:
		try:
			urlopen(path)
		except:
			print("404 Error. Try agein.")
			title_name = input("Type the title you want to download: ")
			path = "http://adultmanga.ru/"+title_name+"/vol1/1?mature=1"
		else:
			res = 1
	url_path = urlMaking(title_name)
	for i in range(1, ch_num+1):
		tmpFileMake(url_path, i)
		contents = ""
		f_page = open("tmp.txt", "r", encoding="utf-8-sig")
		contents = f_page.read()
		start_s = contents.find("var pictures")
		end_s = contents.find(";", start_s)
		contents = contents[start_s:end_s]
		images = []
		p = re.compile('"(.*?)"')
		images = p.findall(contents)
		print(i)
		fetch_files(images, i, title_name)
