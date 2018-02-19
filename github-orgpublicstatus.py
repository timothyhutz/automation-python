"""written by Timothy Hutz timothyhutz@gmail.com
Purpose of this python script is to use the github API to check public status of repos.."""

import github
import sys
import csv


class Repodata_Github(object):
    def __init__(self):
        try:
            self.git_session = github.Github(login_or_token=token)
        except Exception as message:
            print(message)
            exit(1)
        self.repolist = []
        # Builds inital list from all repos in the listed Orginization.
        for data in self.git_session.get_organization(login=org).get_repos():
            self.repolist.append(data.full_name)

    # This is the main that loads each repo private status True or False Boolen
    def main(self):
        reporesults = {}
        for repo in self.repolist:
            repobool = self.git_session.get_repo(full_name_or_id=repo).private
            reporesults[repo] = repobool
        return reporesults


# Primary init if called as source and not module.
if __name__ == '__main__':
    # preset global params
    args = {}
    for item in sys.argv[1:]:
        key, val = item.split('=')
        args[key] = val
    token = args['token']
    org = args['org']
    returndata = Repodata_Github().main()

    with open('data.csv', 'w') as csvfile:
        fieldnames = ['repo name', 'private']
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writeheader()
        for key, value in returndata.items():
            writer.writerow({'repo name': key, 'private': value})
