from typing import Dict, Protocol
import os
from aws_cdk import (
    aws_ec2 as ec2,
    aws_kms as kms
)
from constructs import Construct
from utils.stack_util import add_tags_to_stack


class Ec2Win(Construct):

    def __init__(self, scope: Construct, id: str,
                 config: Dict,
                 vpc: ec2.IVpc,
                #  sg_id: str,
                 ec2_key_name: str,
                 ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        rel_path = "user_data_win/user_data_win.ps1"
        abs_file_path = os.path.join(script_dir, rel_path)

        with open(abs_file_path) as f:
            user_data_win = f.read()

        machine_image=ec2.MachineImage.latest_windows(
            version=ec2.WindowsVersion.WINDOWS_SERVER_2019_ENGLISH_FULL_BASE,
            user_data=ec2.UserData.add_commands(self, user_data_win))

        # genericWindows = ec2.MachineImage.generic_windows(
        #             {
        #                 'us-east-1': 'ami-97785bed',
        #                 'eu-west-1': 'ami-12345678',
        #             }, user_data=ec2.UserData.custom(user_data)
        #         )

        self.winmachine = ec2.Instance(self, "WindowsEc2", 
                instance_type=ec2.InstanceType(instance_type_identifier="t2.small"),
                machine_image=machine_image,
                vpc=vpc,
                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.ISOLATED),
                key_name=ec2_key_name, 
                instance_name="test",
                # security_group=ec2.SecurityGroup.from_security_group_id(self, "secGrp", security_group_id=sg_id),
            )

