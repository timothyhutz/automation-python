"""written by Timothy Hutz timothyhutz@gmail.com
Purpose of this python script is to use the github API to check public status of repos.."""

import github
import sys
import csv

# This is the main that loads each repo private status True or False Boolen
def main(repolist):
	reporesults = {}
	for repo in repolist:
		repobool = git_session.get_repo(full_name_or_id=repo).private
		reporesults[repo]=repobool
	return reporesults

#Builds inital list from all repos in the listed Orginization.
def repolistbuild(org):
	for data in git_session.get_organization(login=org).get_repos():
		repolist.append(data.full_name)

#preset global params
args = {}
for item in sys.argv[1:]:
	key, val = item.split('=')
	args[key]=val
token = args['token']
org = args['org']
repolist = []

try:
	git_session = github.Github(login_or_token=token)
except Exception as message:
	print(message)
	exit(1)

repolistbuild(org)
main(repolist)
with open('data.csv', 'w') as csvfile:
	fieldnames = ['repo', 'private']
	writer = csv.DictWriter(csvfile, fieldnames)
	writer.writeheader()
	for key, value in repolist.items():
		writer.writerow({'repo': key, 'private': value})
