# Simple Webhook #
This code implements a simple webhook for a Github repository in
Python. Once the webhook is configured for PUSH or ISSUES on a Github
repository and the payload URL is setup each of these events will
trigger a call to the script. You can run the script either on your
local development machine using ngrok or as an AWS lambda function.
Currently implemented are PUSH, ISSUES and ISSUE_COMMENT events.

## Development Environment ##
You'll need to make sure you have `python 3.6` and `pipenv` installed.

## Install Patched Webhook Library ##
Due to Zappa bug #1188 it doesn't process the content type for JSON
correctly if it is spelled like this:

    'content-type': 'application/json'

It only recognizes the spelling like this:

    'Content-Type': 'application/json'

As a workaround we need to install a patched `webhook` library.

``
pipenv install -e \
git+https://github.com/lispmeister/python-github-webhook.git@zappa-json-force-content-type#egg=private
``

This forces the content type to JSON. It is unsafe and can lead to
runtime exceptions.

## Install Patched Zappa Library ##
Alternatively you can use this patched version of Zappa until the
patch is merged into the next Zappa release.

``
pipenv install -e \
git+https://github.com/lispmeister/Zappa.git#egg=private
``

# Local Testing with Ngrok #
## Install Ngrok ##
Download and install into $HOME/bin or /usr/local/bin.
<https://ngrok.com/download>

## Start Ngrok ##
Start the ngrok daemon and note down the URL:

    ngrok http 5000

Output

    Session Status                online
    Session Expires               7 hours, 59 minutes
    Version                       2.2.8
    Region                        United States (us)
    Web Interface                 http://127.0.0.1:4040
    Forwarding                    http://5318c304.ngrok.io -> localhost:5000
    Forwarding                    https://5318c304.ngrok.io -> localhost:5000

## Configure the Webhook ##
You'll need to copy the forwarding URL into the payload URL field for
the webhook of your Github repository. See the following web page for
instructions:
<https://developer.github.com/webhooks/configuring/>

Your payload URL should look something like this:
https://5318c304.ngrok.io/postreceive

Your webhook is configured at the path `postreceive` awaiting data.

## Start the Webhook ##
Change into the `simple_webhook` directory and issue the following
commands:

    pipenv install
    pipenv shell
    export FLASK_APP=simple_webhook.py
    flask run --host=0.0.0.0

## Test the Webhook ##
### Push ###
Checkout your Github project, modify a file, commit the file, push
the changes to Github. You should see some console output stating

    Got push event with: <JSON data>

### Create Issue ###
Open the issues page for your git repository on Github and create an
issue. Once the issue is created your webhook will be called and you
should see some output on the console where you started the webhook on
your local machine.

    Got issues with: <JSON data>

### Create a Issue Comment ###
Open the issues page for your git repository on Github and comment on
the issue you just created. Your webhook will be called and you
should see some output on the console where you started the webhook on
your local machine.

    Got issue_comment with: <JSON data>


# Deploying to AWS Lambda #
## Create an IAM Role ##
Go to the AWS console and create a separate IAM role under your AWS
account for your lambda experiments.
Go to the permissions pane for the user and grant the following
permissions via an AWS managed policy:
- AWSLambdaFullAccess
- AmazonS3FullAccess
- AmazonSQSFullAccess

## Add Keys ##
Add the keys for the role to your credentials file in `$HOME/.aws/credentials`.
Example entry:

    [lambda] # using the keypair for the Lambda-user
    access_key_id = <key id>
    aws_secret_access_key = <secret access key>
    aws_access_key_id = <access key id>

## Configure Zappa ##
Change into the `simple_webhook` directory and issue the following
commands:

    pipenv install
    pipenv shell
    zappa init

Make sure you specify your IAM role during the init process. Choose
`us-east-1` as the default region. Zappa will generate the S3 bucket
name for you and will also create the bucket at first deployment.
After initialization your `zappa_settings.json` file should look
similar to this:

    {
        "dev": {
            "app_function": "simple_webhook.app",
            "aws_region": "us-east-1",
            "profile_name": "lambda",
            "project_name": "simple-webhook",
            "runtime": "python3.6",
            "s3_bucket": "zappa-pxizg6md2"
        }
    }

## Start Lambda Service ##
Deploy the webhook service like this:

    zappa deploy dev

After the deploy (which creates the S3 bucket to store the code when
you run it for the first time) Zappa will show the URL for the
service in the last line of the output:

    Deployment complete!: https://m8auwlqzm4.execute-api.us-east-1.amazonaws.com/dev


## Configure the Webhook ##
You'll need to copy the lambda endpoint URL into the payload URL field for
the webhook of your Github repository. See the following web page for
instructions:
<https://developer.github.com/webhooks/configuring/>

For AWS lambda your payload URL should look something like this:
<https://m8auwlqzm4.execute-api.us-east-1.amazonaws.com/dev/postreceive>

Your webhook is configured at the path `postreceive` awaiting data.

## Zappa Tracing ##
You can display a trace of the service calls like this:

    zappa tail

## Test the Webhook ##

### Push ###
Checkout your Github project, modify a file, commit the file, push
the changes to Github. You should see some console output stating

    Got push event with: <JSON data>

### Create Issue ###
Open the issues page for your git repository on Github and create an
issue. Once the issue is created your webhook will be called and you
should see some output on the console where you started the webhook on
your local machine.

    Got issues with: <JSON data>

### Create a Issue Comment ###
Open the issues page for your git repository on Github and comment on
the issue you just created. Your webhook will be called and you
should see some output on the console where you started the webhook on
your local machine.

    Got issue_comment with: <JSON data>
