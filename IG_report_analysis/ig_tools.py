import os, sys, subprocess
from bs4 import BeautifulSoup as soup


# Get the IG profile report file, extract and execute the script passing the path, (replace '\' with '/')
# Example: $ python3 <programName>.py "C:/Users/elp0r/Downloads/iguser_45465465"



# ===============[ Functions ]===============
class IGTools():
	def __init__(self, path=sys.argv[1]):
		self.dataPath = path
		self.files = self.getHTMLFiles()

	# Load config file
	def getFileExtension(self, path):
		return path.split(".")[-1]

	def getHTMLFiles(self):
		self.files = os.popen(f"dir {self.dataPath} /B /S").read().split("\n")[:-1]
		

	# Menu options
	def parseData(self):
		print(self.dataPath)
		content = None

		# Get followers
		with open(f"{self.dataPath}/followers_and_following/followers.html", 'r') as fd:
			content = fd.read()
		self.pageFollowers = soup(content, 'html.parser')
		# Get following
		with open(f"{self.dataPath}/followers_and_following/following.html", 'r') as fd:
			content = fd.read()
		self.pageFollowing = soup(content, 'html.parser')


	
		# Store data
		self.followersList = self.pageFollowers.findAll("a")
		self.followingList = self.pageFollowing.findAll("a")


	def dontFollowMeBack(self):
		unfollowers = []
		for user in self.followingList:
			if user not in self.followersList:
				unfollowers.append(user.text)

		return unfollowers

	def iDontFollowBack(self):
		unfollowed = []
		for user in self.followersList:
			if user not in self.followingList:
				unfollowed.append(user.text)
				
		return unfollowed





# ===============[ Main loop ]===============
if __name__ == '__main__':
	tool = IGTools()
	tool.parseData()
	
	print("Serving CLI Menu")

	while 1:
		os.system('cls')
		print(" + Instagram tools:\n")
		print("\t1 - Followers and unfollowers")
		print("\t\t11 - Get users not folling me back")
		print("\t\t12 - Get user I dont follow back")

		opt = int(input("\nChoose an option: "))

		if (opt == 11): # Users not following me back
			i=1
			print("[i] Users dont follow me back:")
			for user in tool.dontFollowMeBack():
				print(f"\t[{i}] {user}")
				i+=1
		elif (opt == 12): # Users i dont follow back
			i=1
			print("[i] Users I dont follow back:")
			for user in tool.iDontFollowBack():
				print(f"\t[{i}] {user}")
				i+=1
		
		else:
			print("[!] Invalid option...")

		print("\t", end='')
		os.system("pause")
		