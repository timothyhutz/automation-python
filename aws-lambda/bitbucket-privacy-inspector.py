"""Written by Timothy Hutz, timothyhutz@gmail.com
This inspects the security settings via bitbucket API call for whether a repo is public or not.."""

import logging
import requests
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def main(event):
	logger.info(event['repos'])
	for repo in event['repos']:

