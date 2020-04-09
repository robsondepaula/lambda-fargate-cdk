import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="lambda_fargate",
    version="0.0.1",

    description="An empty CDK Python app",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="author",

    package_dir={"": "lambda_fargate"},
    packages=setuptools.find_packages(where="lambda_fargate"),

    # There is no need for you to update 'requirement.txt" just add the dependency on the next array and then do the 'pip install -r requirements.txt'
    install_requires=[
        "aws-cdk.core==1.32.0",
        "aws-cdk.aws-ec2",
        "aws-cdk.aws-lambda",
        "aws-cdk.aws-ecs",
        "aws-cdk.aws-iam",
        "boto3"
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
