#!/usr/bin/python
# encoding: utf-8

# todo: create install script to ensure python modules are installed
# todo: prompt for github user if config doesn't exist
# todo: allow git command to be passed in
# todo: remove hardcoding to config path 


import requests, subprocess, os, sys, string, getpass, getopt
from os.path import expanduser
try:
    import json
except ImportError:
    import simplejson as json 


CONFIG_LOCATION = "config.json"


""" prints the version """
def print_version():
	print 'grcb v0.1'


""" prints the help usage """
def print_usage():
	print 'usage: grcb [-v | -h]'
	print 'Options and arguments:'
	print '-v     : show version info'
	print '-h     : print help / usage'


""" loads the configuration """
def load_config(configFileLocation):
    config = None
    try:
        configOpen = open(configFileLocation, 'r')
        config = json.load(configOpen)
        configOpen.close()
        
    except Exception, e:
        print e
        raise Exception("error loading configfile located at " + configFileLocation )

    return config


""" validates and sets up the args/config for the script """
def process_args(args):
	if len(args) == 0:
		print_usage()
		sys.exit()

	try:
		opts, args = getopt.getopt(args,'vh')
	except getopt.GetoptError:
		print_usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-v':
			print_version()
			sys.exit()
		elif opt == '-h':
			print_usage()
 			sys.exit()

	return load_config(CONFIG_LOCATION)


""" gets a list of all the repo names for the organization """
def get_repo_names(gituser):
	repo_names = []
	url = 'https://api.github.com/orgs/' + gituser['organization'] + '/repos?type=all&per_page=100'

	while url:
		r = requests.get(url, auth=(gituser['username'], gituser['password']))
		try:
			url = r.links['next']['url']
		except KeyError, e:
			url = None

		if(r.ok):
			repos = r.json()
		
			for repo in repos:
				repo_names.append(repo['full_name'])

	return repo_names


""" executes the specified git command across all repos found """
def exec_git_cmd(repo, cmd):
	print
	print 'repo  : ' + repo
	dirname = expanduser('~') + '/workspace/' + string.split(repo, '/')[1] + '/'

	try:
		pr = subprocess.Popen(['/usr/bin/git ' + cmd],
			cwd=os.path.dirname(dirname),
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			shell=True
			)
		(out, error) = pr.communicate()

	except Exception, e:	
		print 'error : ' + str(e)

	else:
		print 'out   : ' + str(out)


""" yep, this is main() """
def main(args):
	config = process_args(args)
	repos = get_repo_names(config['gituser'])

	for repo in repos:
		exec_git_cmd(repo, 'status')
			

""" did I really put a comment here? """
if __name__ == '__main__':
	main(sys.argv[1:])

