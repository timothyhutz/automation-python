"""This is a quick python tool to insure repos are set to private...
Written by Timothy Hutz timothyhutz@gmail.com

HAS ONLY BEEN VERFIED working with github and bitbucket..."""

import csv
import requests

with open('repo.csv') as csvfile:
	repo_detail = csv.DictReader(csvfile)
	for row in repo_detail:
		try:
			print(row['Repo'])
			header = {
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko)'
			}
			url = requests.get(row['Git Endpoint'], headers=header, allow_redirects=True)
			print(url.url, url.status_code, url.history)
			print('\n')
		except Exception as message:
			print(message)


