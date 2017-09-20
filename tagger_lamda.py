import boto3

#All Classes builds here




#Set Params here.
region = 'us-west-2' #input("Region? Press any key to skip. Will use default config: ")
profile = 'grc-sandbox' #input("Profile? Press any key to skip. Will use default config: ")
creds = boto3.Session(profile_name=profile)