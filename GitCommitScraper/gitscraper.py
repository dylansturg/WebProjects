import urllib.request
import urllib.parse
import requests
import json
from requests.auth import HTTPBasicAuth

gitapi = "https://api.github.com/"

def scrapeAllCommits(name, user, passw, histogram, types):
	scraper = GitScraper(user, passw)
	gitUser = scraper.requestGitUser(name)
	if gitUser.user() != user:
		#error on web request
		print("requesting user failed")
		return False

	try:
		gitRepos = scraper.requestGitUserRepos(gitUser)
		for repo in gitRepos:
			gitCommits = scraper.requestGitCommits(repo, gitUser)
			for commit in gitCommits:
				commit.parseStats(types, histogram)
			print("repo %s finished" % repo.repoName())
	except Exception:
		print("failure during scraping")

	return histogram


class GitScraper:
	auth = None

	def __init__(self, user, passw):
		self.auth = HTTPBasicAuth(user, passw)

	def requestGitUser(self, name):
		resp = requests.get(gitapi+"users/"+name, auth=self.auth)
		GitScraper.checkRateLimit(resp)
		resp = resp.json()
		return GitUser(resp)

	def requestGitUserRepos(self, gituser):
		resp = requests.get(gitapi+"users/"+gituser.user()+"/repos", auth=self.auth)
		GitScraper.checkRateLimit(resp)
		resp = resp.json()
		gitrepos = []
		for r in resp:
			gitrepos.append(GitRepo(r))
		return gitrepos

	def requestGitCommits(self, gitrepo, gituser):
		commits = requests.get(gitapi+"repos/"+gituser.user() + "/" + gitrepo.repoName() + "/commits?" + urllib.parse.urlencode([("author", gituser.user())]), auth=self.auth)
		GitScraper.checkRateLimit(commits)
		commits = commits.json()
		gitcommits = []
		for c in commits:
			resp = requests.get(gitapi+"repos/"+gituser.user() + "/" + gitrepo.repoName() + "/commits/" + c["sha"], auth=self.auth)
			GitScraper.checkRateLimit(resp)
			resp = resp.json()
			gitcommits.append(GitCommit(resp))
		return gitcommits

	def checkRateLimit(response):
		if int(response.headers.get('x-ratelimit-remaining', 60)) < 5:
			print("Nearly out of requests!")
		return


def extractExtension(filename):
	import os
	return os.path.splitext(filename)[1][1:]

class GitUser:
	gitdata = None

	def __init__(self, gitdata):
		self.gitdata = gitdata

	def user(self):
		return self.gitdata["login"]

class GitRepo:
	gitdata = None

	def __init__(self, data):
		self.gitdata = data

	def repoName(self):
		return self.gitdata["name"]

class GitCommit:
	gitdata = None

	def __init__(self, data):
		self.gitdata = data

	def parseStats(self, fileTypeMap, histogram):
		files = self.getFiles();
		for f in files:
			extension = extractExtension(f["filename"])
			codeType = fileTypeMap.getCodeType(extension)
			if histogram.get(codeType, None) == None:
				histogram[codeType] = FileTypeLog(codeType)
			histogram[codeType].appendCommitFile(f)


	def getFiles(self):
		return self.gitdata["files"]


class FileTypeMap:
	fileTypes = None
	missingTypes = []

	def __init__(self, configFile):
		f = open(configFile)
		self.fileTypes = json.load(f)
		f.close()

	def getCodeType(self, extension):
		code = self.fileTypes.get(extension.lower(), None)
		if code == None:
			self.missingTypes.append(extension)
			code = "Imaginary"
		return code

class FileTypeLog:
	delta = 0
	additions = 0
	deletions = 0
	fileCount = 0
	codeType = ""

	def __init__(self, code):
		self.codeType = code

	def appendCommitFile(self, f):
		self.additions += f["additions"]
		self.deletions += f["deletions"]
		self.delta += f["additions"] - f["deletions"]
		self.fileCount += 1
