from typing import Dict

from aws_cdk import (
    core,
    aws_ec2 as ec2,
)
from utils.stack_util import add_tags_to_stack
from .auto_ec2 import AutoEc2
# from .eks import Eks

class ComputeStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str,
                 config: Dict,
                 vpc: ec2.IVpc,
                 es_sg_id: str,
                #  env:core.Environment,
                 ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Apply common tags to stack resources.
        add_tags_to_stack(self, config)

        # Get elasticsearch security group created in tne network stack
        es_sg = ec2.SecurityGroup.from_security_group_id(
            self,
            "ElasticsearchSG",
            security_group_id=es_sg_id
        )
        print("vpc : ", vpc)
        # first_ec2_linux = AutoEc2(self, "autoec2", vpc=vpc, env = env)

        bastion = ec2.BastionHostLinux(self, "myBastion",
                                vpc=vpc,
                                subnet_selection=ec2.SubnetSelection(
                                    subnet_type=ec2.SubnetType.ISOLATED),
                                instance_name="myBastionHostLinux",
                                instance_type=ec2.InstanceType(instance_type_identifier="t2.medium"))

        # Aec2 = AutoEc2(self, id="AutoEC2", vpc=vpc)
        # print(bastion.instance.instance_private_ip)
        # create the kubernetes cluster
        # Eks(self, 'Eks', config, vpc, es_sg)
