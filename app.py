import os 
import argparse
import yaml
import getpass
import re

from utils import Utils

my_utils = Utils()
# main parser
parser = argparse.ArgumentParser()

# sub parser
subparsers = parser.add_subparsers(help='sub-command help')

# parser for config options
parser_conf = subparsers.add_parser('config', help='config help')
parser_conf.add_argument('--action', choices=['new','edit','delete','info','list'], help='action help')

# parser for config options
parser_extract = subparsers.add_parser('extract', help='extract help')
parser_extract.add_argument('--source', required=True, help='source help')
parser_extract.add_argument('--query', required=True, help='query help')
parser_extract.add_argument('--output_format', required=True, choices=['csv','json','xml'], help='output format help')



args = parser.parse_args()


def new_or_edit_source(action):
	source= {}
	if action=='new':
		print "New config"
		source['conf_name'] = raw_input("Give a name for the new config : ")
		if my_utils.does_config_exist(source['conf_name'],True)== True:
			print "This configuration exists. Use `clde config --action=edit` if you want to make changes."
			return			
	if action=='edit':
		print "Edit config"
		source['conf_name'] = raw_input("Give the name of the config you want to edit : ")
		if my_utils.does_config_exist(source['conf_name'])==False:
			return

	source['server_type'] = raw_input("Server type (pg/msql) : ").lower()
	source['host'] = raw_input("Host name : ")
	source['port'] = raw_input("Port : ")
	source['database'] = raw_input("Database name : ")
	source['user'] = raw_input("User name : ")
	source['password'] = getpass.getpass("Password (you will not see this): ")

	yaml.dump(source,file(my_utils.config_dir+'/'+source['conf_name'].lower()+'.yml', 'w'))	

def delete_source():
	config = raw_input("Give the name of config you want to delete: ").lower()
	if my_utils.does_config_exist(config)==True:
		os.remove(my_utils.config_dir+'/'+config+'.yml')
		print "Configuration for %s deleted." %(config)	

def get_config_info(config):
	if my_utils.does_config_exist(config)==True:
		config_file = open(my_utils.config_dir+'/'+config+'.yml', "r")
		values = yaml.load(config_file)
		return values  	
	else:
		return False 

def show_config_info():
	config = raw_input("Give the name of config you want to see information : ").lower()
	values = get_config_info(config)
	if values is not False: 
		print '-------------------------------------'
		# Why not a loop or list comp here. yaml serialize alphabatical order when dumps.
		# I don't want to write more code to overwrite that behaviour.  
		# So I output as I want. 
		print  "Config Name : " + values['conf_name']
		print  "Server Type : " + values['server_type']
		print  "Host : " + values['host']
		print  "Port : " + values['port']
		print  "Database : " + values['database']
		print  "User : " + values['user']
		print '-------------------------------------'


def list_sources():
	configs = os.listdir(my_utils.config_dir)
	for each in configs:
		match = re.search(r'yml$',each)
		if match is not None:
			print each.split('.')[0]


def extract(source,query,output):
	if my_utils.does_config_exist(source)==True:
		values = get_config_info(source)
		if values is not False:
			if os.path.exists(args.query):
				print "I'm a file"
			elif args.query.split(' ')[0].lower()=="select":
				print "I'm a query string"
			else:
				print "It looks like the query file you have given does not exist. Please chech your file name."
	else:
		return

if args.__contains__('action'):
	my_action = args.action

	if my_action=='new' or my_action=='edit':
		new_or_edit_source(my_action)

	if my_action=='delete':
		delete_source()

	if my_action=='info':
		show_config_info()

	if my_action=='list':
		list_sources()

if args.__contains__('source') and args.__contains__('query') and args.__contains__('output_format'):
	extract(args.source, args.query, args.output_format)


