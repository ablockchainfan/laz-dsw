from constructs import Construct
from stacks.compute_stack.ec2_win import Ec2Win
from typing import Dict, Protocol
import os
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
)
from utils.stack_util import add_tags_to_stack
from .auto_ec2 import AutoEc2
# from .eks import Eks
key_name = "id_rsa"  # Setup key_name for EC2 instance login 

class ComputeStack(Stack):

    def __init__(self, scope: Construct, id: str,
                 config: Dict,
                 vpc: ec2.IVpc,
                 sg_id: str,
                 ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Apply common tags to stack resources.
        add_tags_to_stack(self, config)

        bastion = ec2.BastionHostLinux(self, "myBastion",
                                vpc=vpc,
                                subnet_selection=ec2.SubnetSelection(
                                    subnet_type=ec2.SubnetType.ISOLATED),
                                instance_name="myBastionHostLinux",
                                instance_type=ec2.InstanceType(instance_type_identifier="t2.medium"))

        
        ec2_1 = Ec2Win(self, "myEc2-1", config=config, vpc=vpc, ec2_key_name=key_name)
        
        ec2_1.winmachine.add_security_group(ec2.SecurityGroup.from_security_group_id(
                    self, "sg1", security_group_id=sg_id, allow_all_outbound=True
                ) )
        

        # ec2_2 = Ec2Win(self, "myEc2-2", config=config, vpc=vpc, ec2_key_name=key_name)
        # ec2_2.winmachine.add_security_group(ec2.SecurityGroup.from_security_group_id(
        #             self, "sg2", security_group_id=sg_id, allow_all_outbound=True
        #         ) )
               

        # ec2_3 = Ec2Win(self, "myEc2-3", config=config, vpc=vpc, ec2_key_name=key_name)
        # ec2_3.winmachine.add_security_group(ec2.SecurityGroup.from_security_group_id(
        #             self, "sg3", security_group_id=sg_id, allow_all_outbound=True
        #         ) )

