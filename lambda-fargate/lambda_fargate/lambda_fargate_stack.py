from aws_cdk import (
    core,
    aws_lambda
)
from aws_cdk.aws_ec2 import (
    Vpc,
    Subnet,
    CfnInternetGateway,
    CfnVPCGatewayAttachment,
    CfnRouteTable,
    CfnRoute,
    CfnSubnetRouteTableAssociation,
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
                         max_azs=1)

        # Public Subnet
        public_subnet_id = "FargateSubnet"
        public_subnet = Subnet(self, public_subnet_id,
                               availability_zone=public_vpc.availability_zones[0],
                               cidr_block="10.0.0.0/24",
                               vpc_id=vpc_id,
                               map_public_ip_on_launch=True)

        # Internet Gateway
        gateway_id = "FargateIGW"
        internet_gateway = CfnInternetGateway(self, gateway_id)
        internet_gateway_attachment = CfnVPCGatewayAttachment(self, "FargateAttachGateway",
                                                              vpc_id=vpc_id,
                                                              internet_gateway_id=gateway_id)

        # Routing
        route_table_id = "FargateRouteTable"
        route_table = CfnRouteTable(self, route_table_id, vpc_id=vpc_id)
        route = CfnRoute(self, "FargateRoute",
                         route_table_id=route_table_id,
                         destination_cidr_block="0.0.0.0/0",
                         gateway_id=gateway_id)
        subnet_table_association = CfnSubnetRouteTableAssociation(self, 'FargateRouteTableAssociation',
                                                                  subnet_id=public_subnet_id,
                                                                  route_table_id=route_table_id
                                                                  )

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
