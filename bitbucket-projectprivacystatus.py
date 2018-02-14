import requests
import csv
import sys

# Primary work data class that's callable if used in module format.
class Repodata_Bitbucket(object):
	# initializes variables to zero and sets the proper project URL
	def __init__(self):
		self.api_url = 'https://' + domain + '/rest/api/1.0/projects/' + project_key
		# start page for inital data load at 0
		self.page_range = [0]
		self.repodata = {}

	# does the pagination calls to retrieve all data for repos including nextpage to the next list.
	def main(self):
		# Counter for bitbucket's paging setup.. Grabs the nextPageStart number and adds it to list...
		for page_num in self.page_range:
			call = requests.get(self.api_url + '/repos?start={}'.format(page_num), auth=(username, password)).json()
			for repo in call['values']:
				# sets only the data I need, repo name and public status
				self.repodata[repo['name']]=repo['public']
			## If we hit the last page end the loop for appending to page_range value.
			if call['isLastPage'] is False:
				self.page_range.append(call['nextPageStart'])
		return self.repodata

# setup for called as direct source and not as module
if __name__ == '__main__':
	args = {}
	for item in sys.argv[1:]:
		key, val = item.split('=')
		args[key] = val

	domain = args['domain']
	project_key = args['project_key']
	username = args['username']
	password = args['password']
	data = Repodata_Bitbucket().main()
	# writes out the CSV file
	with open('data.csv', 'w') as csvfile:
		fieldnames = ['repo name', 'public']
		writer = csv.DictWriter(csvfile, fieldnames)
		writer.writeheader()
		#Pairs the Dictonary items into seperate namespaces
		for key, value in data.items():
			writer.writerow({'repo name': key, 'public': value})
