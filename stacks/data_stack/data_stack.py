from typing import Dict

from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_rds as rds, 
    aws_secretsmanager as sm,
    aws_kms as kms,
)
import aws_cdk as core
import json

from aws_cdk.aws_kms import Key
from constructs import Construct
from utils.stack_util import add_tags_to_stack
# from .elasticsearch import Elasticsearch
# from .rds_db import RDSStack

class DataStack(Stack):
    vpc: ec2.IVpc

    def __init__(self, scope: Construct, id: str,
                 config: Dict,
                 vpc: ec2.Vpc,
                 es_sg_id: str,
                 kms_key: Key,
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
        # secretName = "mssql-db-secret"
        instanceIdentiffier = "mymssql"

        # json_template = {'username':'admin'}
        # db_creds = sm.Secret(
        #     self, 'db-secret-pword',
        #     description="Password for MSSQL",
        #     secret_name= secretName,
        #     generate_secret_string=sm.SecretStringGenerator(
        #         include_space=False,
        #         password_length=12,
        #         generate_string_key="rds-pwd",
        #         exclude_punctuation=True,
        #         secret_string_template=json.dumps(json_template)
        #     )
        # )
        # mydb_parameter_group = rds.ParameterGroup(self, "ParameterGroup", 
        #         engine=rds.DatabaseInstanceEngine.sql_server_web(
        #             version=rds.SqlServerEngineVersion.VER_14
        #         ), 
        #         parameters={
        #             'open_cursors': '100'
        #         }
        #     )

        self.rdsSql = rds.DatabaseInstance( 
            self, "RDS-MSSQL",
            engine=rds.DatabaseInstanceEngine.sql_server_web(
                version=rds.SqlServerEngineVersion.VER_14
            ), 
            credentials=rds.Credentials.from_generated_secret("admin"),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.ISOLATED),
            # port=3306,
            instance_type= ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3,
                ec2.InstanceSize.SMALL,
            ),
            removal_policy=core.RemovalPolicy.DESTROY,
            deletion_protection=False,
            multi_az=False,
            backup_retention=core.Duration.days(0),
            #     from_password(
            #     username="admin",
            #     password=db_creds.secret_value_from_json("rds-pwd")
            # ),
            instance_identifier= instanceIdentiffier,
            copy_tags_to_snapshot=True,
            # parameter_group=mydb_parameter_group
            storage_encryption_key=kms_key
        )
        self.endPointAddress = self.rdsSql.db_instance_endpoint_address
        # rdsSql.add_proxy("proxy",   )
        self.rdsSql.add_rotation_single_user(automatically_after=core.Duration.days(3))
        

        # rdsSql.connections.allow_default_port_from(es_sg_id, "Allow from security group")