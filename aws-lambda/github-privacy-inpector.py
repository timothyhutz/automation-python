""" Written by Timothy Hutz timothyhutz@gmail.com for inspecting github repos
the intention of this code is to be used with Lambda but can be customized with any
serverless architecture"""

import pip
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
try:
	import github
except ImportError:
	pip.main(['install', 'pygithub'])
	logging.info('pygithub was not in python3.6 modules, it was added so you can use it')
	import github
except Exception as message:
	logger.debug(message)

def main(event, context):
	repolist = event['repos']
	git_session = github.Github(login_or_token=event['username'], password=event['password'])
