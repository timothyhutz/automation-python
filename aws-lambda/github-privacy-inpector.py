""" Written by Timothy Hutz timothyhutz@gmail.com for inspecting github repos
the intention of this code is to be used with Lambda but can be customized with any
serverless architecture"""

import logging
logging.basicConfig()
import pip
try:
	import pygithub
except ImportError:
	pip.main(['install', 'pygithub'])
	logging.info('pygithub was not in python3.6 modules, it was added so can use it')
	import github

def main(event, context):
	repo_list = event['repos']