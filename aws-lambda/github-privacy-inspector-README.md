<h1> Setup and use </h1>
<p> Github-privacy-inspector </p>

This piece of code is designed only to work with AWS lambda and AWS APIgate way.
Its is designed to test the repo name against whether it is setup
as a private repo or open to the public..

You must send the full repo name which is usually like this
\<owner\>/\<repo\>
\
timothyhutz/automation-python


Setting up a APIGateway with a GET method attached on the lambda
function will be required. This will need to be a application/json context.
Please follow this documentation to setup your APIgateway for this Lambda function.
https://docs.aws.amazon.com/apigateway/latest/developerguide/getting-started-lambda-non-proxy-integration.html


You will need to setup API token in github security settings and you will need to have
permissions to the Repos you want to lookup.

<h2> Pygithub module packaging </h2>

Since lambda only include the core modules and boto3, you will need to package up
the pygithub module and this piece of code into a zip file for upload..
This is called building a deployment package. If you don't do this you will get a 
failure on the import statement for github.

Here is the aws instructions on building deployment packges for lambda pyhton function with 
third party modules(libraries).

https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html



<h3>Usage after APIgateway setup</h3>

The event stream will pass a json body to the main handler.
the only two things that should be passed via a GET method are

Github API token which is a JSON string..

Repos which are a JSON list of github repos.

Example....

{

    "token": "<token>",
    "repos":[
        "<repo>",
        "<repo>"
    ]

}

Here is the repose you should get which should be a 200,
True means it is private..

{

	"REPO NAME": true,
	"REPO NAME": true,
	"REPO NAME": true

}