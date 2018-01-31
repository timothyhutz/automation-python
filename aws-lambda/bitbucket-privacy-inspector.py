"""Written by Timothy Hutz, timothyhutz@gmail.com
This inspects the security settings via bitbucket API call for whether a repo is public or not.."""

import logging
import boto3
import requests
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def main(event):
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
		for repo in call['values']:
			logger.info(repo)
			##DB lookup check to see if it exist
			response = dbtable.get_item(
				Key={
					'repo': repo['name']
				}
			)
			## if Key error (which means does not exist) then put data in table.
			try:
				response['Item']
			except KeyError:
				logger.info(repo['name'] + ' not found adding to DB')
				dbtable.put_item(
					Item={
						'repo': repo['name'],
						'public': bool(repo['public'])
					}
				)
			## If we hit the last page end the loop for appending to pagestart value.
		if call['isLastPage'] is False:
				page_range.append(call['nextPageStart'])
		break

