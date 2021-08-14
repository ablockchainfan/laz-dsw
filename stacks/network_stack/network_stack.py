from typing import Dict

from aws_cdk import (
    core,
    aws_ec2 as ec2,
)
from utils.stack_util import add_tags_to_stack
from .vpc import Vpc
from .security_group import SecurityGourp
from .tgw import Tgw
from .tgw_attach import TgwAttach


class NetworkStack(core.Stack):
    vpc: ec2.IVpc
    es_sg_id: str

    def __init__(self, scope: core.Construct, id: str, config: Dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Apply common tags to stack resources.
        add_tags_to_stack(self, config)

        vpcConstruct = Vpc(self, 'Vpc', config)
        self.vpc = vpcConstruct.vpc

        sg = SecurityGourp(self, "SecurityGroups", self.vpc)
        self.es_sg_id = sg.es_sg.security_group_id

        # core.CfnOutput(self, "dsw-vpc-id", value=self.vpc.vpc_id )
        # core.CfnOutput(self, "dsw-es-sg-id", value= self.es_sg_id)
        
        # tgwConstruct = Tgw(self, 'Tgw', config )
        # laz_tgw_id = config['network']['tgw']['id']
        # if not laz_tgw_id:
        #     tga = TgwAttach(self, 'tgw_attachment_vpc1', tgw_id=laz_tgw_id, vpc=self.vpc, config=config )
        # else:
        #     print("TGW not specified")
        # tga = TgwAttach(self, 'tgw_attachment_vpc1', tgw_id=tgwConstruct.TransitGateway.ref,vpc=self.vpc, config=config )

        # tga.TransitGatewayAttachment.add_depends_on(tgwConstruct.TransitGateway)
        
        # bastion = ec2.BastionHostLinux(self, "myBastion",
        #                         vpc=self.vpc,
        #                         subnet_selection=ec2.SubnetSelection(
        #                             subnet_type=ec2.SubnetType.ISOLATED),
        #                         instance_name="myBastionHostLinux",
        #                         instance_type=ec2.InstanceType(instance_type_identifier="t2.large"))

