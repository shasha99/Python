from paramiko imoport socket

class PollSocket(object):
	def __init__(sleepTime,timeout):
		self.__sleepTime = sleepTime
		self.__timeout   = timeout
	
	@property
	def sleepTime(self):
		return self.__sleepTime
	
	@property
	def timeout(self):
		return self.__timeout
	
	@__sleepTime.setter
	def sleepTime(self,val):
		self.sleepTime = val
		
	@__timeout.setter
	def timeout(self,val):
		self.timeout = val
		
	@staticmethod
	def __isSocketActive(host,port):
		s = socket()
		try:
			s.connect((host,port))
		except socket.error as e:
			return False
		else:
			return True

	

	def pollSocket(host,port):
		counter = int(60/self.sleepTime) * self.nMinutesToWait 
	
		for i in range(counter):
			if Utility.__isSocketActive(host,port):
				return True
			else:
				time.sleep(sleepTime)
		return False

	
if __name__=="__main__":
	#sleepTime in seconds and timeout in minutes.
	p = PollSocket(10,6)
	if p.pollSocket("localhost",8080):
		print("Success")
	else:
		print("Failure")
	
