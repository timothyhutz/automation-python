""" Written by Timothy Hutz timothyhutz@gmail.com for inspecting github repos
the intention of this code is to be used with Lambda but can be customized with any
serverless architecture"""

import pip
import json
import logging
logger=logging.getLogger()
logger.setLevel(logging.INFO)
try:
	import github
except ImportError:
	pip.main(['install', 'pygithub'])
	logging.info('pygithub was not in python3.6 modules, it was added so you can use it')
	import github
except Exception as message:
	logger.error(message)

def main(event, context):
	repolist = event['repos']
	reporesults = {}
	logger.info(print(repolist))
	git_session = logger.info(github.Github(login_or_token=event['username'], password=event['password']))
	for repo in repolist:
		repodata = json.loads(git_session.get_repo(full_name_or_id=repo))
		reporesults[repo]=repodata['']
	return reporesults
