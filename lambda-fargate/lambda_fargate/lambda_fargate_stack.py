from aws_cdk import (
    core,
    aws_lambda as aws_lambda
)
from aws_cdk.aws_ec2 import (
    Vpc,
    SubnetConfiguration,
    SubnetType,
    SecurityGroup,
    Peer,
    Port
)
from aws_cdk.aws_ecs import (
    Cluster,
    FargateTaskDefinition,
    ContainerImage,
    AwsLogDriver
)
from aws_cdk.aws_iam import (
    Role,
    ServicePrincipal,
    ManagedPolicy,
    Policy,
    PolicyStatement
)


class LambdaFargateStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Public VPC
        vpc_id = "FargateVPC"
        public_vpc = Vpc(self, vpc_id,
                         cidr="10.0.0.0/16",
                         enable_dns_support=True,
                         enable_dns_hostnames=True,
                         max_azs=1,
                         nat_gateways=0,
                         subnet_configuration=[SubnetConfiguration(
                             subnet_type=SubnetType.PUBLIC,
                             name="Public",
                             cidr_mask=24
                         )])

        # Security Group
        security_group = SecurityGroup(
            self,
            "FargateSG",
            vpc=public_vpc
        )
        security_group.add_ingress_rule(
            peer=Peer.ipv4("127.0.0.1/32"),
            connection=Port.all_traffic()
        )

        # define an ECS cluster hosted within the requested VPC
        cluster = Cluster(self, "cluster", vpc=public_vpc)

        # define our task definition with a single container
        # the image is built & published from a local asset directory
        task_role = Role(
            self, 'FargateTaskRole',
            assumed_by=ServicePrincipal('ecs-tasks.amazonaws.com')
        )
        task_role.add_managed_policy(
            ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AmazonECSTaskExecutionRolePolicy"
            )
        )

        task_definition = FargateTaskDefinition(
            self, "SimpleTask", execution_role=task_role, task_role=task_role)
        task_definition.add_container("SimpleContainer",
                                      image=ContainerImage.from_asset(
                                          "docker_with_task"),
                                      environment={
                                          "LAMBDA_NAME": "", "REQUEST_ID": ""
                                      },
                                      logging=AwsLogDriver(stream_prefix="ecs"))

        # lambda that triggers the Fargate Task
        lambda_role = Role(
            self, 'RunFargateTaskRole',
            assumed_by=ServicePrincipal('lambda.amazonaws.com')
        )
        lambda_role.add_managed_policy(
            ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSLambdaBasicExecutionRole"
            )
        )
        Policy(
            self, 'LambdaToFargate',
            policy_name='LambdaToFargate',
            statements=[PolicyStatement(
                actions=["ecs:RunTask"],
                resources=[task_definition.task_definition_arn]),
                PolicyStatement(
                actions=["iam:PassRole"],
                resources=[task_role.role_arn])],
            roles=[lambda_role],
        )

        lambda_function = aws_lambda.Function(self, "RunFargateLambda",
                                              handler="lambda_function.handler",
                                              runtime=aws_lambda.Runtime.PYTHON_3_7,
                                              code=aws_lambda.Code.asset(
                                                  "function"),
                                              role=lambda_role
                                              )
        lambda_function.add_environment("ECSCluster", cluster.cluster_arn)
        lambda_function.add_environment(
            "ECSTaskArn", task_definition.task_definition_arn)
        lambda_function.add_environment(
            "ECSSubnet", public_vpc.public_subnets[0].subnet_id)
        lambda_function.add_environment(
            "ECSSecGroup", security_group.security_group_id)
