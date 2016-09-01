import os 
import argparse
import yaml
import getpass
import re

from utils import Utils
from config import Config
from extract import Extract

my_utils = Utils()
my_config = Config()
my_extract = Extract()

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

if args.__contains__('action'):
	my_action = args.action

	if my_action=='new' or my_action=='edit':
		my_config.new_or_edit_source(my_action)

	if my_action=='delete':
		my_config.delete_source()

	if my_action=='info':
		my_config.show_config_info()

	if my_action=='list':
		my_config.list_sources()

if args.__contains__('source') and args.__contains__('query') and args.__contains__('output_format'):
	my_extract.extract(args.source, args.query, args.output_format)


