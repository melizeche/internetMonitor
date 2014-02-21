#!/usr/bin/env python
import sqlite3, datetime, time, os, urllib2
from apscheduler.scheduler import Scheduler

#path to sqlite database
DB = "up.db"

#connect db
def connectDB():
	try:
		conn = sqlite3.connect(DB)
		return conn
	except sqlite3.OperationalError, msg:
		print msg
		pass

def createTable():
	conn = connectDB()
	c = conn.cursor()
	try:
		c.execute('''CREATE TABLE upordown
        	     ( id INTEGER PRIMARY KEY   AUTOINCREMENT,date text, updown boolean)''')
		conn.commit()
		conn.close()
	except sqlite3.OperationalError, msg:
		print msg
		pass
	

#return timestamp
def now():
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	return st

#insert into db if this time the fucking internet is available or not
def insertRow(up):
	conn = connectDB()
	c = conn.cursor()
	timestamp = now()
	c.execute("INSERT INTO upordown ('date','updown') VALUES ('%s', '%s')" % (timestamp,  up) )
	conn.commit()
	conn.close()	

#checks if a url is reacheable
def isUp(url):
    try:
        urlfile = urllib2.urlopen(url)
        status_code = urlfile.code
        if status_code in (200, 302):
            return 'up', urlfile
    except:
        pass
    return 'down', None

#checks if google and yahoo are down == NO INTERNET FOR YOU
def tigoMeCojeOno():#drunk now fix later
    google, fileGoogle = isUp('http://www.google.com')
    yahoo, fileYahoo = isUp('http://www.yahoo.com')
    if google == 'down' and yahoo == 'down':
        return False
    return True

def extract():
	conn = connectDB()
	c = conn.cursor()
	lista = c.execute('SELECT * FROM upordown WHERE updown="True"')
	up = len(lista.fetchall())
	lista = c.execute('SELECT * FROM upordown WHERE updown="False"')
	down = len(lista.fetchall())
	lista = c.execute('select * from upordown order by rowid asc limit 1; ')
	first = lista.fetchone()[1]
	lista = c.execute('select * from upordown order by rowid desc limit 1; ')
	last = lista.fetchone()[1]

	return up,down, first, last

def writeData():
	up, down, first, last = extract()
	try:
		f = open("data.js", "w")
		try:
			f.write('var first = "%(first)s";\nvar last = "%(last)s";\nvar up = %(up)i;\nvar down = %(down)i;' % locals()) # Write a string to a file
		finally:
			f.close()
	except IOError:
		pass

#cron function
def job_function():
	print "Comprobando " + now()
	insertRow(tigoMeCojeOno())
	writeData()


#set the scheduler to 1 minuto interval
sched = Scheduler()
sched.start()
sched.add_interval_job(job_function, minutes=1)	

def main():
	print "Hola cada un minuto voy a comprobar si hay internet o no"
	if not os.path.isfile(DB):
		createTable()
	insertRow(False)
	while True:
	    time.sleep(10)



if __name__ == "__main__":
    main()
