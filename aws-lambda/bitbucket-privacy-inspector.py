"""Written by Timothy Hutz, timothyhutz@gmail.com
This inspects the security settings via bitbucket API call for whether a repo is public or not.."""

import logging
import boto3
import requests
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def main(event, context):
	#setting the DB info
	dynamodb = boto3.resource('dynamodb')
	dbtable = dynamodb.Table('bitbucket_data')
	##API url build out..
	api_url = 'https://' + event['domain'] + '/rest/api/1.0/projects/' + event['project_key']
	#start page for inital data load at 0
	page_range = [0]
	## Empty Dict for repos
	repo_data = {}
	## Counter for bitbucket's pageing setup.. Grabs the nextPageStart number and adds it to list...
	for page_num in page_range:
		call = requests.get(api_url + '/repos?start={}'.format(page_num), auth=(event['username'], event['password'])).json()
		if call['isLastPage'] is False:
				page_range.append(call['nextPageStart'])
		break

