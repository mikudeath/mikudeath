import os
import mysql.connector
from time import localtime
from mysql.connector import MySQLConnection, Error

def lastMessage():
		try:
			conn = mysql.connector.connect(host="localhost",
				database="chat",
				user="root",
				password="vertrigo")
			cursor = conn.cursor()
			cursor.execute("SELECT * FROM `chat` ORDER BY `id` DESC LIMIT 1")

			row = cursor.fetchone()
			while row is not None:
				print("[{0}]<{1}> {2}".format(row[1], row[3], row[2]))
				row = cursor.fetchone()
			cursor.close()
			conn.close()
		except Error as err:
			print(err)


def printChat():
	try:
		conn = mysql.connector.connect(host="localhost",
			database="chat",
			user="root",
			password="vertrigo")
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM `chat`")
		
		row = cursor.fetchone()
		
		while row is not None:
			print("[{0}]<{1}> {2}".format(row[1], row[3], row[2]))
			row = cursor.fetchone()
		cursor.close()
		conn.close()
	except Error as err:
		print(err)

def addToChat():
	message = input()
	d = localtime()
	curTime = "{0}.{1}.{2} - {3}.{4}.{5}".format(d[2], d[1], d[0], d[3], d[4], d[5])
	username = "PyTester"
	try:
		conn = mysql.connector.connect(host="localhost",
			database="chat",
			user="root",
			password="vertrigo")
		cursor = conn.cursor()
		cursor.execute("INSERT INTO `chat`(`datetime`,`contents`,`username`) VALUES('{0}', '{1}', '{2}')".format(curTime, message, username))

		lastMessage()
	except Error as err:
		print(err)

printChat()
while True:
	addToChat()
