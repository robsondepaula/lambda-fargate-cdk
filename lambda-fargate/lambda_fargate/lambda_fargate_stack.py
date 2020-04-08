from aws_cdk import (
    core,
    aws_lambda
)
from aws_cdk.aws_ec2 import (
    Vpc,
    SubnetConfiguration,
    SubnetType,
    SecurityGroup,
    Peer,
    Port
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
        security_group_id = "FargateSG"
        security_group = SecurityGroup(
            self,
            id=security_group_id,
            vpc=public_vpc,
            security_group_name=security_group_id
        )
        security_group.add_ingress_rule(
            peer=Peer.ipv4("127.0.0.1/32"),
            connection=Port.all_traffic()
        )
