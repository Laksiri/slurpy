import os 
import argparse
import yaml
import getpass
import re

from utils import Utils
from config import Config

my_utils = Utils()
my_config = Config()

class Extract():

	def __init__(self):
		pass

	def extract(self,source,query,output):
		if my_utils.does_config_exist(source)==True:
			values = my_config.get_config_info(source)
			if values is not False:
				if os.path.exists(query):
					sql_strings = self.read_sql_file(query)
					for each_query in sql_strings:
						if self.is_sql_string_safe(each_query) ==True:
							print 'I can process you'
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
		if first_word == 'select' or first_word == 'with':
			return True
		else:
			return False	 



		