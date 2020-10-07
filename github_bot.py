from github import Github
import sys
import os
from threading import Thread
import random
from PIL import Image

class git_module(object):
	def __init__(self,username,password):
		self.g = Github(username,password)
		self.user = self.g.get_user()
		self.commit = f"new random commit {random.randint(1000,9999) }"

	def create_repo(self,name):
		self.repo = self.user.create_repo(name)

	def select_repo(self,name):
		self.name = name
		try :
			self.repo = self.user.get_repo(name)
		except :
			raise Exception(f'reposetory \' {self.name } \' not found ')

	def create_file(self,filename,filedata):
		self.repo.create_file(filename,self.commit,filedata)

	def update_files(self,content,updated_data):
		# def update_files(self,filename,updated_data):
		# content = self.repo.get_content(filename)
		self.repo.update_file(content.path,self.commit,updated_data,content.sha)

	def delete_file(self,contents,commit='delete file' ):
		self.repo.delete_file(contents.path, commit, contents.sha)


	def all_content_of_repo(self):
		try :
			contents = self.repo.get_contents("")
		except :
			contents = []
			# print('no content ')
			return contents

		all_files = []
		def file_recursion(contents):
			for i in contents:
			    if i.type == "dir":
			    	file_recursion(self.repo.get_contents(i.path))
			    else:
			    	all_files.append(i)


		file_recursion(contents)

		return all_files

	def all_content_of_dir(self):
		device_files = []
		for currentdir,folder,files in os.walk(os.path.join(default_project_dir,self.reponame)):
			if files == [] :
				continue
			else:
				for i in files:
					device_files.append(os.path.join(currentdir,i))

		for index,data in enumerate(device_files):
			# print(index,data)
			replace = device_files[index].split(os.path.join(default_project_dir,self.reponame))[-1]
			device_files[index] = replace.replace('\\','/').replace('/','',1)

		return device_files

	def read_file(self,file):
		try:
			path = os.path.join(self.working_dir,file.replace('/','\\'))
			with open(path,'r') as f:
				return f.read()
		except :
			raise Exception("unable to read this file format")

	def isupdate_require(self,file):
		self.read_file()


	@classmethod
	def check_updates(cls,username,password,reponame):
		cls.reponame = reponame
		cls.default_project_dir = default_project_dir
		cls.working_dir = os.path.join(default_project_dir,reponame)

		# executed on any any update files
		existing_file = []
		new_file = []
		to_delete_file = []
		git = cls(username,password)
		git.select_repo(reponame)
		all_repo_files = git.all_content_of_repo()
		all_device_file = git.all_content_of_dir()

		# check the presence of the git files in device
		for file in all_repo_files :
			if file.path in all_device_file:
				# file exits may need to update
				existing_file.append(file)

			else :
				# file to delete
				to_delete_file.append(file)

		for file in all_device_file:
			# all new files which are not on git 
			if file not in [i.path for i in all_repo_files ] :
				new_file.append(file)

		# print(existing_file)
		if existing_file:
			print('\nUPDATING files')
			for index,i in enumerate(existing_file) :
				print(index ,'updating file',i.path)
				git.update_files(i,git.read_file(i.path))



		# print(new_file)
		if new_file:
			print('\nCREATING NEW files')
			for index,i in enumerate(new_file) :
				print(index ,'creating file',i)
				# create new files
				git.create_file(i,git.read_file(i))


		# print(to_delete_file)
		if to_delete_file:
			print('\nDELETEING files')
			for index,i in enumerate(to_delete_file) :
				# delete file
				print(index ,'delete file',i.path)
				git.delete_file(i)


		# print(all_repo_files)
		# print(all_device_file)


	@classmethod
	def new_project(cls,username,password,reponame):
		# create a new file and repo on git
		cls.reponame = reponame
		os.chdir(default_project_dir)
		try :
			os.mkdir(reponame)
		except:
			print('\n##############################################\nfolder of same name alread exits !!!!!\n\nunable to complete the task   !!!!!!!')
			return

		os.chdir(reponame)

		# run your code editor
		os.system('code .')

		# print(os.getcwd())
		git = cls(username,password)
		git.create_repo(reponame)

if __name__ == '__main__':
	username = ''   # save your username here
	password = '' # save your password here
	default_project_dir = 'D:\\'   # Your folder in your pc where you store all of your project

	# python module_name commend name
	try :
		file_name , commend, project_name = sys.argv
		if commend == 'create_repo' and project_name :
			git_module.new_project(username,password,project_name)
		
		elif commend == 'update_repo' and project_name :
			git_module.check_updates(username,password,project_name)
	
		else:
			raise Exception('WRONG input ')
	except :
		raise Exception('\n\nWRONG format try :- python <filename> <commend> <project_name>\nthere are two commends \n1. create_repo \n2. update_repo ')
