A retake on [mixing AWS Lambda and Fargate](https://github.com/robsondepaula/lambda-fargate) but now using AWS CDK.

## Prerequisites

If you are unfamiliar with AWS Cloud Development Kit (AWS CDK) I recommend investing sometime on the following [AWS workshop](https://cdkworkshop.com/).

Once you have the prerequisites made for using AWS CDK on Python, go to the next section.

## Constructing

Navigate to the CDK project location.

```
$ cd lambda-fargate
```

Use the following step to activate your virtualenv.

```
$ source .env/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .env\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

In case this is the first time your are running CDK on your AWS Profile (Account/Region), install the bootstrap stack on it.

```
$ cdk bootstrap
```

If no error messages are shown, deploy the architecture on AWS.

```
$ cdk deploy
```

Once again, enjoy all the moving parts.

## Cleanup

If not already, navigate to the CDK project location.

```
$ cd lambda-fargate
```

Perform the decomission of all resources created.

```
$ cdk destroy
```