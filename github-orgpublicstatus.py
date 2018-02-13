"""written by Timothy Hutz timothyhutz@gmail.com
Purpose of this pyhton script is to use the github API to check public status of repos.."""

import github

def main(repos, token):
	reporesults = {}
	for repo in repos:
		repobool = git_session.get_repo(full_name_or_id=repo).private
		reporesults[repo]=repobool
	return reporesults


token = None
try:
	git_session = github.Github(login_or_token=token)
except Exception as message:
	print(message)
	exit(1)
repodata =
repos = []
