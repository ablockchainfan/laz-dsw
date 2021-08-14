from typing import Dict, Protocol
import os
from aws_cdk import (
    core,
    aws_ec2 as ec2,
)
from utils.stack_util import add_tags_to_stack
from .auto_ec2 import AutoEc2
# from .eks import Eks
key_name = "id_rsa"  # Setup key_name for EC2 instance login 

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

        # script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        # rel_path = "user_data/user_data.sh"
        # abs_file_path = os.path.join(script_dir, rel_path)

        # with open(abs_file_path) as f:
        #     user_data = f.read()

        
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        rel_path = "user_data_win/user_data_win.ps1"
        abs_file_path = os.path.join(script_dir, rel_path)

        with open(abs_file_path) as f:
            user_data_win = f.read()

        machine_image=ec2.MachineImage.latest_windows(
            version=ec2.WindowsVersion.WINDOWS_SERVER_2019_ENGLISH_CORE_BASE,
            user_data=ec2.UserData.add_commands(self, user_data_win))

        # genericWindows = ec2.MachineImage.generic_windows(
        #             {
        #                 'us-east-1': 'ami-97785bed',
        #                 'eu-west-1': 'ami-12345678',
        #             }, user_data=ec2.UserData.custom(user_data)
        #         )


        winmachine = ec2.Instance(self, "WindowsEc2", 
                instance_type=ec2.InstanceType(instance_type_identifier="t2.small"),
                machine_image=machine_image,
                vpc=vpc,
                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.ISOLATED),
                key_name=key_name, 
                instance_name="test"
            )

        pub_vpc = ec2.Vpc(
            self,
            "vpc",
            nat_gateways=0,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public", subnet_type=ec2.SubnetType.PUBLIC
                )
            ],
        )

        winmachine = ec2.Instance(self, "WindowsEc2-1", 
                instance_type=ec2.InstanceType(instance_type_identifier="t2.small"),
                machine_image=machine_image,
                vpc=pub_vpc,
                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                key_name=key_name, 
                instance_name="test"
            )



