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


def print_version():
	print 'grcb v0.1'


def print_usage():
	print 'usage: grcb [-v | -h]'
	print 'Options and arguments:'
	print '-v     : show version info'
	print '-h     : print help / usage'


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


def get_repo_names(gituser):
	full_names = []
	# r = requests.get('https://api.github.com/orgs/sparcedge/repos?type=all', auth=(raw_input('Username: '), getpass.getpass()))
	r = requests.get('https://api.github.com/orgs/' + gituser['organization'] + '/repos?type=all', auth=(gituser['username'], gituser['password']))

	if(r.ok):
		repos = r.json()
	
		for repo in repos:
			full_names.append(repo['full_name'])

	return full_names


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


def main(args):
	config = process_args(args)
	repos = get_repo_names(config['gituser'])

	for repo in repos:
		exec_git_cmd(repo, 'status')
			

if __name__ == '__main__':
	main(sys.argv[1:])
