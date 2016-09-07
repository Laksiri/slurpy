import re
import os 


class Utils():

	base_dir = ''
	config_dir = ''

	def __init__(self):
		self.base_dir = os.path.dirname(os.path.abspath(__file__))
		self.config_dir = self.base_dir + "/config"
		if not os.path.exists(self.config_dir):
			os.makedirs(self.config_dir)


	def remove_comments_from_sql_string(self,sql_string):
		# to track the begining of multiline comment: /* */
		block_comment = False
		out =''

		content = sql_string.split('\n')
		for iline in content:
			if iline is not '':
				match = re.match(r'^--',iline)
				if match is None: 
					if block_comment is False:
						match = re.match(r'^\/\*',iline)
						if match is not None:
							 block_comment = True
						else:
							out =out + iline + '\n'

						# what if the comment is like this: /*howdy*/
						match = re.search(r'\*\/$',iline)
				 		if match is not None:
							block_comment = False	

				 	elif block_comment is True:
				 		match = re.search(r'\*\/$',iline)
				 		if match is not None:
							block_comment = False
						else:
							# These two together eliminate this like: /* a goo one */ -- isn't it
							match_1 = re.search(r'\*\/',iline)
							match_2 = re.search(r'--',iline)

							if match_1 is None and match_2 is None:
								out =out + iline + '\n'
							else:
								block_comment = False					 	
		#print out
		return out


	def does_config_exist(self,config,omit_message=False):
		if not os.path.exists(self.config_dir+'/'+config+'.yml'):
			if omit_message==False:
				print "No such configuration exists. you can use `clde config --action=list` to list all configs."
			return False
		else:
			return True

# obj = Utils()
# with open('test.sql') as f:
#     content = f.readlines()
# obj.remove_comments_from_sql_string(content)