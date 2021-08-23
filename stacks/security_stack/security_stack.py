from aws_cdk import (
    aws_ec2 as ec2
)
from constructs import Construct


class SecurityStack(Construct):
    _vpc: ec2.Vpc
    es_sg: ec2.SecurityGroup

    def __init__(self, scope: Construct, id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self._vpc = vpc 
        # self.es_sg = ec2.SecurityGroup(
        #     self, 'Ec2Sg',
        #     security_group_name='Ec2Sg1',
        #     vpc=self._vpc,
        #     description='Security group for EC2 compute',
        #     allow_all_outbound=True
        # )
