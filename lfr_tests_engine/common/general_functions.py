import time
import datetime

def getLocalTimeInDPUFormat():
	tm_year = 2000
	tm_mon = 1
	tm_mday = 1
	tm_hour = 0
	tm_min = 0
	tm_sec = 0
	tm_wday = 5
	tm_yday = 1
	tm_isdst = -1
	t = (tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst)
	referenceTime = time.mktime( t )
	localTime = int( time.time() - referenceTime)
	return localTime

def printMessage( message ):
	now = datetime.datetime.now()
	mSec = int(now.microsecond / 1000)
	print now.strftime('%Y-%m-%d %H:%M:%S.') + str(mSec) + " " + message

def getDateAndTime():
	now = datetime.datetime.now()
	dateAndTime = now.strftime('%Y_%m_%d-%H_%M_%S')
	return dateAndTime

def getDate():
	now = datetime.datetime.now()
	date = now.strftime('%Y_%m_%d')
	return date