# automation-python
Collection of my AWS automation work with python only.

01/29/2018 --> current <br>
Added aws-lambda folder with a github privacy inspector piece. \
every lambda script will get its own MarkDown README to show what I did
and how I set it up and / or how to build it.. 

09/20/2017<br>
Added Tagger, This is a AWS tag creator for declaring ownership. Will create tags of Owner: "data inputed" for ALL AWS EC2 based objects attached to the set VPC. There is a Local
operated version called tagger.py desiged to run on your local system. The other version is called tagger_lambda.py, this version runs with limited console output for AWS Lambda FAAS.

if your running lambda version you will need to fill out three paramaters. <br>
Profile<br>
Region<br>
VPC-Id<br>

07/12/2017<br>
Added transfer-auth0users.py, this is a pyhton app that will pull auth0 users
from one source and push the data into another Auth0 tenant. uses full json and
REST api. It also pulls an API JWT token for authentication via auth0 api.

06/29/2017<br>
Currently have two pieces of work auth0-testusersload.py --> This is designed to "signup" users."number"@email.com into your database for loadtesting or whatever.
alertlogic_install.py --> this autoinstalls alertlogic threatmanager agent into EC2 OS and joins it to your local appliance. Reqiures two arguments <Unique Key> and <Appliance IP>.
