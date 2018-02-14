import requests
import csv
import sys


class Repodata(object):

	def __init__(self):
		self.api_url = 'https://' + domain + '/rest/api/1.0/projects/' + project_key
		# start page for inital data load at 0
		self.page_range = [0]
		self.repodata = {}

	def main(self):
		# Counter for bitbucket's pageing setup.. Grabs the nextPageStart number and adds it to list...
		for page_num in self.page_range:
			call = requests.get(self.api_url + '/repos?start={}'.format(page_num), auth=(username, password)).json()
			for repo in call['values']:
				print(repo)
				self.repodata[repo['name']]=repo['public']
				with open('data.csv', 'w') as csvfile:
					fieldnames = ['repo name', 'public']
					writer = csv.DictWriter(csvfile, fieldnames)
					writer.writeheader()
					for key, value in self.repodata.items():
						writer.writerow({'repo name': key, 'public': value})

			## If we hit the last page end the loop for appending to page_range value.
			if call['isLastPage'] is False:
				self.page_range.append(call['nextPageStart'])
			break


args = {}
for item in sys.argv[1:]:
	key, val = item.split('=')
	args[key] = val

domain=args['domain']
project_key = args['project_key']
username = args['username']
password = args['password']
if __name__ == '__main__':
	start = Repodata()
	start.main()

