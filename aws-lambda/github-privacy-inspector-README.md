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
Please follow this documentation to setup your Lambda APIgateway
https://docs.aws.amazon.com/apigateway/latest/developerguide/getting-started-lambda-non-proxy-integration.html


You will need to setup API token in github security settings and you will need to have
permissions to the Repos you want to lookup.

<h3>Usage after APIgateway setup</h3>

The event stream will pass a json body to the main handler.
the only two thing that should be passed via a GET method are

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