import os 
import argparse
import yaml
import getpass
import re
import hashlib
import time

import pandas as pd
import psycopg2 as pg

from utils import Utils
from config import Config

my_utils = Utils()
my_config = Config()

class Extract():

	CONN = None 
	RUN_FOLDER  = None

	def __init__(self):
		pass

	def extract(self,source,query,output):
		if my_utils.does_config_exist(source)==True:
			values = my_config.get_config_info(source)
			if values is not False:
				self.make_run_folder()
				if os.path.exists(query):
					sql_strings = self.read_sql_file(query)
					i =0 
					for each_query in sql_strings:
						if self.is_sql_string_safe(each_query) ==True:
							print 'I can process you'
							i += 1
							self.write_clean_sql_file(self.RUN_FOLDER +'/clean_sql.sql',each_query,'/*------ QUERY ' + str(i) + ' ------ */')
							self.conect_and_extract(source,each_query,self.RUN_FOLDER,i)
						else:
							print 'sorry, you are not safe'	
				elif query.split(' ')[0].lower()=="select":
					print "I'm a query string"
				else:
					print "It looks like the query file you have given does not exist. Please chech your file name."
		else:
			return

	def read_sql_file(self, file_name):
		sql_strings=[]
		with open(file_name, 'r') as f:
			read_data = f.read()
		if read_data is not '':
			comments_removed = my_utils.remove_comments_from_sql_string(read_data)
			sql_strings = comments_removed.split(';')[:-1] #[:-1] is to remove the empty line at the end 
		return 	sql_strings
	
	def is_sql_string_safe(self, sql_string):
		first_word =sql_string.split(' ')[0].lower()

		print first_word
		if first_word == 'select' or first_word == 'with' or first_word == '\nselect' or first_word == '\nwith':
			return True
		else:
			return False	 

	def conect_and_extract(self,source,query,output_dir,index):
		my_source = my_config.get_config_info(source)
		db_server_type= my_source['server_type']
		db_host= my_source['host']
		db_port= my_source['port']
		db_database= my_source['database']
		db_user= my_source['user'] 
		db_password = my_source['password']


		if db_server_type.lower() == 'pg':
			self.CONN = pg.connect(host=db_host,user=db_user,password=db_password,database=db_database)
			cur =  self.CONN.cursor()
			cur.execute(query)
			my_header = [desc[0].strip() for desc in cur.description]
			df= pd.DataFrame(cur.fetchall())
			df.columns = my_header
			
			df.to_csv(self.RUN_FOLDER +'/output_'+ str(index)+'.csv',index=False)
			self.CONN.close()


	def make_run_folder(self):
		hash = hashlib.sha1()
		hash.update(str(time.time()))
		run_id =  hash.hexdigest() 
		## ugly. ouput should be in somewhere user can access quickly. Change this later.  
		run_folder = os.path.dirname(__file__)+ '/run/' + run_id
		try:
			os.stat(run_folder)
		except:
			os.makedirs(run_folder)

		self.RUN_FOLDER	= run_folder	

	def write_clean_sql_file(self, file_path, sql_string, label):
		with open(file_path,"a+") as f:
			f.write(label+'\n')
			f.write(sql_string+'\n')
			f.write('/*-------------------*/\n\n')	
		f.close()

		# open connection
		# run query and get results to a pandas data frame
		# output pandas dataframe in to requested file type
			# inform user with raw count and out_put file name
		# close connection


		# make a folder for output eachtime. have cleansed sql file with index numbrers in it. 
		# make the output file name as same as the index of the sql string (in the cleansed file.)