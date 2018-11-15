#!/usr/bin/python
#coding=utf-8
import os
import re
import sys
import operator
from commands import *

workspace = '/work2/pie_sku1_ZC600KL_dev'

# TODO:在编译的时候同步上一个版本的manifest到workspace中

projectlist = getoutput('cat .repo/project.list').split('\n')
manifestlist = getoutput('ls manifest_tag_*.xml').split('\n')

change_list = 'change_list.txt'

if os.path.exists(workspace + '/' + change_list) == True:
    os.system('rm -rf %s' % (workspace + '/' + change_list))

changelist = open(workspace + '/' + change_list, 'a+')
changelist.write("[CHANGELIST]:%s to %s\n\n==============================================\n" % (manifestlist[0], manifestlist[1]))
changelist.close()

for project in projectlist:
	search = r"\"" + project + r"\""
	print project
	projectinfo = getoutput('grep %s manifest_tag_*.xml' % search).split('\n')
	commitID = []

	projectname = re.findall((re.compile("<project name=\"(.*?)\"")), projectinfo[0])[0]
	branch = re.findall((re.compile("upstream=\"(.*?)\"")), projectinfo[0])[0]

	for i in projectinfo:
		reg = r'revision="(.{40})'
		pattern = re.compile(reg)
		result = re.findall(pattern,i)
		print 'commitid:%s' %result
		if (operator.ne(result, commitID)):
			commitID.append(result[0])
		else:
			print '%s has no changes, pass!!!!!!!!\n-----------------------------------' % project
	print '%s:%s' %(project, commitID)
	if len(commitID) > 1:
		os.chdir(project)
		changelist = open(workspace + '/' + change_list, 'a+')
		changelist.write("\n-----------------------------------\n[%s]" % project + "\n")
		changelist.close()
		#print '%s;;;;%s' % (commitID[0], commitID[1])
		submitInfo = getoutput("git log %s..%s --format=%s" % (commitID[0], commitID[1], '%H^^^^^%ae^^^^^%ad^^^^^%s')).split('\n')
		#submitInfo = getoutput("git log --pretty=format:\"%H %ae %ad %s\"")
		print submitInfo

		changelist = open( workspace + '/' + change_list, 'a+')
		for item in range(len(submitInfo)):
			context = submitInfo[item].split('^^^^^')
			for index in range(len(context)):
				#print "%s %s............\n" % (item, context[item])
				if index == 0:
					changelist.write("Commit:" + str(context[index]) + "\n")
				elif index == 1:
					changelist.write("Owner:" + str(context[index]) + "\n")
				elif index == 2: 
					changelist.write("Date:" + str(context[index]) + "\n")
				elif index == 3:
					changelist.write("Subject:" + str(context[index]) + "\n")
			changelist.write("Project:" + projectname + "\n")
			changelist.write("Branch:" + branch + "\n\n")
		changelist.close()
		
	os.chdir(workspace)


