#!/usr/bin/env python3

from aws_cdk import core

from lambda_fargate.lambda_fargate_stack import LambdaFargateStack


app = core.App()
LambdaFargateStack(app, "lambda-fargate")

app.synth()
