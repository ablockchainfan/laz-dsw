from typing import Dict, List

from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_s3 as s3
)


class Vpc(core.Construct):
    config: Dict
    vpc: ec2.Vpc
    subnet_configuration: List[ec2.SubnetConfiguration] = []

    def __init__(self, scope: core.Construct, id: str, config: Dict) -> None:
        super().__init__(scope, id)
        self.config = config

        self.__build_subnets_config()
        self.__create_vpc()

    def __create_vpc(self):
        vpc_config = self.config['network']['vpc']
        self.vpc = ec2.Vpc(
            scope=self,
            id=self.config['name'],
            subnet_configuration=self.subnet_configuration,
            max_azs=vpc_config['maxAzs'],
            cidr=vpc_config['cidr'],
            nat_gateways=0,
            # nat_gateway_subnets=ec2.SubnetSelection(
            #     subnet_group_name=vpc_config['natGatewaySubnetName']
            # ),
            enable_dns_hostnames=True,
            enable_dns_support=True 
        )
        self.vpc.add_flow_log(id="flog", 
                            destination=ec2.FlowLogDestination.to_s3(s3.Bucket.from_bucket_arn(self, "FlogBucket", self.config['network']['flowlog-bucket']['url'])),
                            traffic_type=ec2.FlowLogTrafficType.ALL)
        # self.vpc.add_s3_endpoint(id="s3_end_laz")

        self.vpc.add_interface_endpoint(id="com.amazonaws.us-west-1.s3",
                service=ec2.InterfaceVpcEndpointService(
                    name="com.amazonaws.us-west-1.s3", port=443))        

        # self.vpc.add_gateway_endpoint(id="gws3ep",
        #     service=ec2.GatewayVpcEndpointAwsService(name= "s3",
        #             prefix="com.amazonaws" ))
        self.vpc.add_gateway_endpoint('S3Endpoint', 
                        service=ec2.GatewayVpcEndpointAwsService.S3)

        self.vpc.add_interface_endpoint(id="com.amazonaws.ec2",
                service=ec2.InterfaceVpcEndpointService(
                    name="com.amazonaws."+ self.config["awsRegion"] + ".ec2", port=443), private_dns_enabled=True)

        self.vpc.add_interface_endpoint(id="com.amazonaws.ssm",
                service=ec2.InterfaceVpcEndpointService(
                    name="com.amazonaws."+ self.config["awsRegion"] + ".ssm", port=443), private_dns_enabled=True)

        self.vpc.add_interface_endpoint(id="com.amazonaws.ec2messages",
                service=ec2.InterfaceVpcEndpointService(
                    name="com.amazonaws."+ self.config["awsRegion"] + ".ec2messages", port=443), private_dns_enabled=True)

        self.vpc.add_interface_endpoint(id="com.amazonaws.ssmmessages",
                service=ec2.InterfaceVpcEndpointService(
                    name="com.amazonaws."+ self.config["awsRegion"] + ".ssmmessages", port=443), private_dns_enabled=True)


    def __build_subnets_config(self):
        for subnet in self.config['network']['subnets']:
            self.subnet_configuration.append(ec2.SubnetConfiguration(
                name=subnet['name'],
                subnet_type=ec2.SubnetType[subnet['subnetType']],
                cidr_mask=subnet['cidrMask']
            ))
