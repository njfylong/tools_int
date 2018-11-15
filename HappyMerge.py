#!/usr/bin/python
#coding=utf-8
import os
import re
#import sys
import operator
import datetime
import smtplib

from commands import *
from time import *
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class AsusPatchMerge():
	def __init__(self, workspace = '/work1', project = 'ZC554KL'):
		os.chdir(workspace)
		self.__workspace = os.getcwd()
		self.__project = project
		self.__asus_source = self.__project + '-P-' + 'Asus'
		self.__amt_source = self.__project + '-P-' + 'AMT'
		self.__asus_sync_manifest = self.__project + '-P-' + 'Manifest'
		self.__share = 'share'
		self.__asus_patch = self.__project + '-P-' + 'patch'
		self.__asus_patch_backup = 'Patch-Backup'
		
		self.__local_host = '10.20.11.23'
		self.__change_list = 'change_list'
		self.__merged_log = 'Merged-LOG'
		self.__merged_log_file = self.__project + '-' + 'merged.log'
		
		# debug
		self.__debug = False
		self.__push_code_to_git = True
		
		# Email
		self.__mail_sender = 'yanlong.fu@archermind.com'
		if False == self.__debug:
			self.__mail_to = ['huia.xu@archermind.com', 'wen.wang@archermind.com', 'baobin.wu@archermind.com', 'yiwei.zhu@archermind.com']
			self.__mail_receivers = ['yanlong.fu@archermind.com']
			self.__mail_cc = ['lei2.xu@archermind.com', 'huihui.yan@archermind.com', 'jund.wang@archermind.com', 'liming.wang@archermind.com', 'yanlong.fu@archermind.com']
		else:
			self.__mail_to = ['yanlong.fu@archermind.com']
			self.__mail_receivers = ['yanlong.fu@archermind.com']
			self.__mail_cc = ['yanlong.fu@archermind.com']
		
		self.__mail_host = 'smtp.archermind.com'
		self.__mail_port = '25'
		self.__mail_user = 'n002224'
		self.__mail_pwd = 'fyl.123456'

		self.__auto_merged_success = 'SUCCESS'
		self.__auto_merged_fail = 'FAILED'
		
		self.__current_time = ''
		
		self.__sync_git_list = ['vendor/app-prebuilt/' + self.__project, 'vendor/app-prebuilt/config']
		self.__mini_project_list = ['ZC554KL', 'ZD553KL']
		self.__mini_manifest = 'Mini-Manifest'
		self.__telecom_gits = ['packages/services/Telecomm', 'packages/services/Telephony', 'packages/providers/TelephonyProvider', 'packages/services/Mms', 'frameworks/opt/telephony']

        # asus project source code
		if not os.path.isdir(self.__workspace + '/' + self.__asus_source):
		    os.system('mkdir -p %s/%s' % (self.__workspace, self.__asus_source))
		# amt project source code
		if not os.path.isdir(self.__workspace + '/' + self.__amt_source):
		    os.system('mkdir -p %s/%s' %(self.__workspace, self.__amt_source))
        # asus manifest
		if not os.path.isdir(self.__workspace + '/' + self.__asus_sync_manifest):
		    os.system('mkdir -p %s/%s' % (self.__workspace, self.__asus_sync_manifest))
		# share:asus
		if not os.path.isdir(self.__workspace + '/' + self.__share + '/' + self.__asus_source):
		    os.system('mkdir -p %s/%s/%s' % (self.__workspace, self.__share, self.__asus_source))
		# share:asus patch
		if not os.path.isdir(self.__workspace + '/' + self.__share + '/' + self.__asus_patch):
		    os.system('mkdir -p %s/%s/%s' % (self.__workspace, self.__share, self.__asus_patch))
		# patch backup
		if not os.path.isdir(self.__workspace + '/' + self.__asus_patch_backup + '/' + self.__asus_patch):
		    os.system('mkdir -p %s/%s/%s' % (self.__workspace,  self.__asus_patch_backup, self.__asus_patch))
		    
	def __reset(self):
		print "__reset"
		if False == self.__debug:
			os.chdir(self.__workspace + '/' + self.__asus_source)
			os.system('rm -v manifest_tag*.xml; rm -v change_list*.txt')
			if self.__project in self.__mini_project_list:
				os.chdir(self.__workspace + '/' + self.__asus_source + '/' + '.repo/manifests')
				os.system('git reset --hard HEAD')
				os.chdir(self.__workspace + '/' + self.__asus_source)
				for git in self.__sync_git_list:
					print git
					os.system('repo sync -d -c %s' % git)
					print "asus sync done ......."
			else:
				os.system('repo sync -d -c -j12')
			os.chdir(self.__workspace + '/' + self.__share + '/' + self.__asus_source)
			if self.__project in self.__mini_project_list:
				os.chdir(self.__workspace + '/' + self.__share + '/' + self.__asus_source + '/' + '.repo/manifests')
				os.system('git reset --hard HEAD')
				os.chdir(self.__workspace + '/' + self.__share + '/' + self.__asus_source)
				for git in self.__sync_git_list:
					os.system('repo sync -d -c -j12 %s' % git)
			else:
				os.system('repo sync -d -c -j12')
			os.chdir(self.__workspace + '/' + self.__amt_source)
			os.system('repo forall -c "git clean -df; git reset --hard HEAD"')
			if self.__project in self.__mini_project_list:
				for git in self.__sync_git_list:
					os.system('repo sync -d -c -j12 %s' % git)
			else:
				os.system('repo sync -d -c -j12')
			

	def merge_asus_patch(self):
		print "MergeAsusPatch"
		self.__reset()
		os.chdir(self.__workspace + '/' + self.__asus_source)
		self.__current_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
		#self.__currentTime = currentTime
		merged_log = open(self.__workspace + '/' + self.__merged_log + '/' + self.__merged_log_file, 'a+')
		merged_log.write(self.__current_time + '\n')
		merged_log.close()
		if self.__project in self.__mini_project_list:
			os.system('cp -dpRv %s/%s/%s-asus-manifest.xml %s/%s/.repo/manifests/default.xml' % (self.__workspace, self.__mini_manifest, self.__project, self.__workspace, self.__asus_source))
		os.system('repo manifest -ro manifest_tag_%s.xml' % self.__current_time )
		os.system('cd .repo/manifests;git reset --hard HEAD;cd ../..')
		backup_manifest = getoutput('ls %s/%s' % (self.__workspace, self.__asus_sync_manifest)).split('\n')
		if len(backup_manifest) == 0:
			os.system('cp -dpRv manifest_tag_%s.xml  %s/%s/' % (self.__current_time, self.__workspace, self.__asus_sync_manifest))
			exit()
		last_manifest = getoutput('ls %s/%s' % (self.__workspace, self.__asus_sync_manifest)).split('\n')[-1]
		os.system('cp -dpRv %s/%s/%s %s/%s/' %(self.__workspace, self.__asus_sync_manifest, last_manifest, self.__workspace, self.__asus_source))
		compare = getstatusoutput('diff %s manifest_tag_%s.xml' % (last_manifest, self.__current_time))
		if (compare[0] >> 8) != 0 :
			print 'ASUS has changes!!!!!!'
			os.system('cp -dpRv manifest_tag_%s.xml %s/%s/' %(self.__current_time, self.__workspace, self.__asus_sync_manifest))
			os.system('mkdir -p %s/%s/%s/%s' % (self.__workspace, self.__asus_patch_backup, self.__asus_patch, self.__current_time))
		else:
			print 'ASUS has no changes.'
			#os.system('mv -v manifest_tag_%s.xml %s/%s/%s' % (self.__currentTime, self.__baseDir, self.__AsusSourceRepoManifest, lastManifest))
			exit()
		change_git_list = self.make_changelist_and_patch(last_manifest, 'manifest_tag_' + self.__current_time + '.xml', self.__change_list + '_' + self.__current_time + '.txt', self.__current_time)
		print change_git_list
		merged_result = self.merge_patch(self.__current_time, change_git_list)
		if len(change_git_list) > 0:
			self.__copy_patch_to_share(self.__current_time)
			self.__send_mail(self.__current_time, merged_result)
		print "%s run done" % self.__current_time


	def make_changelist_and_patch(self, lastmanifest, currentmanifest, changelist, synctime):
		print "make_changelist_and_patch"
		os.chdir(self.__workspace + '/' + self.__asus_source)
		if self.__project in self.__mini_project_list:
			git_list = self.__sync_git_list
		else:
			git_list = getoutput('cat .repo/project.list').split('\n')
			git_list.remove('dailytag')
		change_list = open(self.__workspace + '/' + self.__asus_source + '/' + changelist, 'a+')
		change_list.write("[CHANGELIST]:%s to %s\n\n==============================================\n" % (lastmanifest, currentmanifest))
		change_list.close()
		change_git_list = []
		for git in git_list:
			search = r"\"" + git + r"\""
			print git
			git_info = getoutput('grep %s manifest_tag_*.xml' % search).split('\n')
			print git_info
			commitID = []
			git_name = re.findall((re.compile("<project name=\"(.*?)\"")), git_info[0])[0]
			print git_name
			git_branch = re.findall((re.compile("upstream=\"(.*?)\"")), git_info[0])[0]
			print git_branch
			for i in git_info:
				reg = r'revision="(.{40})'
				pattern = re.compile(reg)
				result = re.findall(pattern, i)
				if (operator.ne(result, commitID)):
					commitID.append(result[0])
				else:
					print '%s has no changes, pass.\n-----------------------------------' % git
			print '^^^^^^%s:%s^^^^^^' %(git, commitID)
			if len(commitID) == 0:
				exit()
			if len(commitID) > 1:
				os.chdir(git)
				print "%s has changes!!!!!!!!" % git
				os.system('mkdir -p %s/%s/%s/%s/%s' % (self.__workspace, self.__asus_patch_backup, self.__asus_patch, self.__current_time, git))
				# format patch
				os.system('git clean -df')
				os.system('git format-patch %s..%s' % (commitID[0], commitID[-1]))
				os.system('cp -dpRv *.patch %s/%s/%s/%s/%s'  % (self.__workspace, self.__asus_patch_backup, self.__asus_patch, self.__current_time, git))
				change_git_list.append(git)
				change_list = open(self.__workspace + '/' + self.__asus_source + '/' + changelist, 'a+')
				change_list.write("\n-----------------------------------\n[%s]" % git + "\n")
				change_list.close()
				#print '%s;;;;%s' % (commitID[0], commitID[1])
				submit_info = getoutput("git log %s..%s --format=%s" % (commitID[0], commitID[1], '%H^^^^^%ae^^^^^%ad^^^^^%s')).split('\n')
				#submitInfo = getoutput("git log --pretty=format:\"%H %ae %ad %s\"")
				print submit_info
				change_list = open(self.__workspace + '/' + self.__asus_source + '/' + changelist, 'a+')
				for item in range(len(submit_info)):
					context = submit_info[item].split('^^^^^')
					for index in range(len(context)):
						if index == 0:
							change_list.write("Commit:" + str(context[index]) + "\n")
						elif index == 1:
							change_list.write("Owner:" + str(context[index]) + "\n")
						elif index == 2: 
							change_list.write("Date:" + str(context[index]) + "\n")
						elif index == 3:
							change_list.write("Subject:" + str(context[index]) + "\n")
					change_list.write("Project:" + git_name + "\n")
					change_list.write("Branch:" + git_branch + "\n\n")
				change_list.close()
			os.chdir(self.__workspace + '/' + self.__asus_source)
		os.system('cp -dpRv %s %s/%s/%s/%s' % (changelist, self.__workspace, self.__asus_patch_backup, self.__asus_patch,  self.__current_time))
		os.chdir(self.__workspace + '/' + self.__asus_patch_backup + '/' + self.__asus_patch + '/' + self.__current_time)
		os.system('tar czvf %s.tar ./' % self.__current_time)
		os.chdir(self.__workspace)
		return change_git_list
		
	
	def merge_patch(self, synctime, changegitlist):
		print "merge_patch"
		os.chdir(self.__workspace + '/' + self.__amt_source)
		if self.__project in self.__mini_project_list:
			os.system('cp -dpRv %s/%s/%s-amt-manifest.xml .repo/manifest.xml' % (self.__workspace, self.__mini_manifest, self.__project))
		os.system('rm -v manifest_tag.xml; repo manifest -ro manifest_tag.xml')
		os.system('cd .repo/manifests;git reset --hard HEAD;cd ../..')
		merged_result = {}
		for git in changegitlist:
			os.chdir(git)
			branch = self.__get_git_branch(git, self.__workspace + '/' + self.__amt_source + '/' + 'manifest_tag.xml')
			if True == self.__push_code_to_git:
				apply_patch = getstatusoutput('git am %s/%s/%s/%s/%s/*.patch' % (self.__workspace, self.__asus_patch_backup, self.__asus_patch, self.__current_time, git))	
				#apply_patch = getstatusoutput('ls')
				if (apply_patch[0] >> 8) == 0:
					push_status = getstatusoutput('git push origin HEAD:refs/for/%s' % branch)
					#push_status = getstatusoutput('ls')
					if (push_status[0] >> 8) == 0:
						merged_result[git] = self.__auto_merged_success
					else:
						merged_result[git] = self.__auto_merged_fail
				else:
					merged_result[git] = self.__auto_merged_fail
					os.system(' git am --abort;git reset --hard HEAD^')				
				print "%s patch merge done." % git
			os.chdir(self.__workspace + '/' + self.__amt_source)				
		return merged_result
	        
	        
	def __get_git_branch(self, git, manifest):
		search = r"\"" + git + r"\""
		git_info = getoutput('grep %s %s' % (search, manifest)).split('\n')
		print git_info
		branch = re.findall((re.compile("upstream=\"(.*?)\"")), git_info[0])[0]
		print branch
		return branch

        
 	def __copy_patch_to_share(self, synctime):
		print "__copy_patch_to_share"
		if not os.path.isdir(self.__workspace + '/' + self.__share + '/' + self.__asus_patch + '/' + synctime):
			os.system('mkdir -p %s/%s/%s/%s' % (self.__workspace, self.__share, self.__asus_patch, synctime))
		os.system('cp -dpRv %s/%s/%s/%s/*.tar %s/%s/%s/%s/' % (self.__workspace, self.__asus_patch_backup, self.__asus_patch, synctime, self.__workspace, self.__share, self.__asus_patch, synctime))
		       


	def __send_mail(self, synctime='', mergedresult=None):
		print "__send_mail"
		mailBody = []
		mailBody.append('<p align=\'Left\'><b>Hi 各位,</b></p>')
		mailBody.append('<p>&nbsp; &nbsp;&nbsp;<strong>Asus %s</strong>&nbsp;has&nbsp;updated&nbsp; at %s, refer to:</p>' % (self.__project, synctime))
		mailBody.append('<h4><strong>[Change List]</strong></h4>')
		mailBody.append('<p>attachment</p>')
		mailBody.append('<h4><strong>[Asus Patch]</strong></h4>')
		mailBody.append('<p>%s:%s/%s/%s/%s/%s.tar</p>' % (self.__local_host, self.__workspace, self.__share, self.__asus_patch, synctime, synctime))
		mailBody.append('<h4><strong>[Asus Code]</strong></h4>')
		mailBody.append('<p>%s:%s/%s/%s</p>' % (self.__local_host, self.__workspace, self.__share, self.__asus_source))
		mailBody.append('<h4><strong>[Merged Status]</strong><span style="color:red;background-color:gray;">---以下 FAILED 的模块需要手动合入, 合入后请基于此邮件回复!</span></h4>')
		for key, value in mergedresult.items():
			if value == self.__auto_merged_fail:
				if key in self.__telecom_gits:
					mailBody.append('%s: %s---<strong>@朱以为</strong><br />' % (key, value))
				else:
					mailBody.append('%s: %s---<strong>@许辉</strong><br />' % (key, value))
			else:
				mailBody.append('%s: %s<br />' % (key, value))
		mailBody.append('<p></p>')
		mailBody.append('<p>PS:此邮件为脚本工具自动发送, 相关问题请联系:付燕龙</p><br />')
		mail = MIMEMultipart('related')
		mailText = MIMEText(''.join(mailBody).encode('gb2312'), 'html','gb2312')
		mail['Subject']= '[AUTOMERGE][%s P] %s'  % (self.__project, synctime)
		mail['From'] = self.__mail_sender
		mail['To'] = ','.join(self.__mail_to)
		mail['Cc'] = ','.join(self.__mail_cc)
		mail.attach(mailText)
		change_list = MIMEApplication(open(self.__workspace + '/' + self.__asus_patch_backup + '/' + self.__asus_patch + '/' + synctime + '/' + self.__change_list + '_' + synctime + '.txt', 'rb').read())
		change_list.add_header('Content-Disposition', 'attachment', filename=self.__change_list + '_' + synctime + '.txt')
		mail.attach(change_list)
		smtp = smtplib.SMTP()
		smtp.connect(self.__mail_host, self.__mail_port)
		smtp.login(self.__mail_user, self.__mail_pwd)
		smtp.sendmail(self.__mail_sender, self.__mail_to + self.__mail_cc, mail.as_string())
		smtp.quit()


if __name__ == "__main__":
	pm = AsusPatchMerge(sys.argv[1], sys.argv[2])
	pm.merge_asus_patch()




















