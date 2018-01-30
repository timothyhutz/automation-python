""" Written by Timothy Hutz timothyhutz@gmail.com for inspecting github repos
the intention of this code is to be used with Lambda but can be customized with any
serverless architecture"""

import logging
logger=logging.getLogger()
logger.setLevel(logging.INFO)
import github


def main(event):
	reporesults = {}
	logger.info(event['repos'])
	try:
		git_session = github.Github(login_or_token=event['token'])
	except Exception as message:
		logger.error(message)
		exit(1)
	for repo in event['repos']:
		repobool = git_session.get_repo(full_name_or_id=repo).private
		reporesults[repo]=repobool
	return reporesults
