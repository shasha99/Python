
@staticmethod
def __isSocketActive(host,port):
	s = socket()
try:
	s.connect((host,port))
except socket.error as e:
	return False
else:
	return True

	
@staticmethod
def pollSocket(host,port):

	#we will be polling after every 10 seconds and will wait for maximum 10 minutes.
	sleepTime = 10 # In seconds
	
	nMinutesToWait = 10 #In minutes
	
	counter = int(60/sleepTime) * nMinutesToWait 
	
	for i in range(counter):
		if Utility.__isSocketActive(host,port):
			return True
		else:
			#wait for 10 seconds.
			time.sleep(10)
	return False
