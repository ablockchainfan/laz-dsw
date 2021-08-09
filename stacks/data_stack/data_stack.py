from typing import Dict

from aws_cdk import (
    aws_ec2 as ec2,
    aws_rds as rds, 
    aws_secretsmanager as sm,
    core,
)
import json
from utils.stack_util import add_tags_to_stack
# from .elasticsearch import Elasticsearch
# from .rds_db import RDSStack

class DataStack(core.Stack):
    vpc: ec2.IVpc

    def __init__(self, scope: core.Construct, id: str,
                 config: Dict,
                 vpc: ec2.Vpc,
                 es_sg_id: str,
                 ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Apply common tags to stack resources.
        add_tags_to_stack(self, config)

        # Get elasticsearch security group created in tne network stack
        # es_sg = ec2.SecurityGroup.from_security_group_id(
        #     self,
        #     "ElasticsearchSG",
        #     security_group_id=es_sg_id
        # )

        # Create Elasticsearch cluster
        # Elasticsearch(self, 'Vpc', config, vpc, es_sg)
        # RDSStack(self, "RDSStack", vpc)
        json_template = {'username':'admin'}
        db_creds = sm.Secret(
            self, 'db-secret-pword',
            description="Password for MSSQL",
            secret_name= "mssql-db-secret",
            generate_secret_string=sm.SecretStringGenerator(
                include_space=False,
                password_length=12,
                generate_string_key="rds-pwd",
                exclude_punctuation=True,
                secret_string_template=json.dumps(json_template)
            )
        )
        rdsSql = rds.DatabaseInstance(
            self, "RDS",
            engine=rds.DatabaseInstanceEngine.sql_server_web(
                version=rds.SqlServerEngineVersion.VER_14
            ), 
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.ISOLATED),
            # port=3306,
            instance_type= ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3,
                ec2.InstanceSize.LARGE,
            ),
            removal_policy=core.RemovalPolicy.DESTROY,
            deletion_protection=False,
            multi_az=False,
            backup_retention=core.Duration.days(0),
            credentials=rds.Credentials.from_password(
                username="admin",
                password=db_creds.secret_value_from_json("rds-pwd")
            ),
            instance_identifier="mymssql",
            copy_tags_to_snapshot=True
        )
        self.endPointAddress = rdsSql.db_instance_endpoint_address
