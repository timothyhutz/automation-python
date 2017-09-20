# automation-python
Collection of my AWS automation work with python only.

09/20/2017
Added Tagger, This is a AWS tag creator for declaring ownership. Will create tags of Owner: <data inputed> for ALL AWS EC2 based objects attached to the set VPC. There is a Local
operated version called tagger.py desiged to run on your local system. The other version is called tagger_lambda.py, this version runs with limited console output for AWS Lambda FAAS.

if your running lambda version you will need to fill out three paramaters. 
Profile
Region
VPC-Id

06/29/2017
Currently have two pieces of work auth0-testusersload.py --> This is designed to "signup" users."number"@email.com into your database for loadtesting or whatever.

alertlogic_install.py --> this autoinstalls alertlogic threatmanager agent into EC2 OS and joins it to your local appliance. Reqiures two arguments <Unique Key> and <Appliance IP>.

07/12/2017 --> Current

Added transfer-auth0users.py, this is a pyhton app that will pull auth0 users
from one source and push the data into another Auth0 tenant. uses full json and
REST api. It also pulls an API JWT token for authentication via auth0 api.
