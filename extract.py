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
					print "I'm a file"
				elif query.split(' ')[0].lower()=="select":
					print "I'm a query string"
				else:
					print "It looks like the query file you have given does not exist. Please chech your file name."
		else:
			return