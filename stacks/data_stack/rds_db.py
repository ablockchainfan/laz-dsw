#!/usr/bin/env python3

from aws_cdk import (
    aws_ec2 as ec2,
    aws_rds as rds, 
    aws_secretsmanager as sm,
)
import aws_cdk as core
import json

class RDSStack(core.NestedStack):
    def __init__(self, app: core.App, id: str, vpc, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        # vpc = ec2.Vpc(self, "VPC")
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
                secret_string_template=json.dump(json_template)
            )
        )
        rdsSql = rds.DatabaseInstance(
            self, "RDS",
            database_name="db1",
            engine=rds.DatabaseInstanceEngine.sql_server_web(
                version=rds.SqlServerEngineVersion.VER_14
            ), 
            vpc=vpc,
            # port=3306,
            instance_type= ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3,
                ec2.InstanceSize.MICRO,
            ),
            removal_policy=core.RemovalPolicy.DESTROY,
            deletion_protection=False,
            multi_az=False,
            backup_retention=core.Duration.days(0),
            credentials=rds.Credentials.from_password(
                username="admin",
                password=db_creds.secret_value_from_json("rds-pwd")
            ),
            instance_identifier="mymssql"
        )
        self.endPointAddress = rdsSql.db_instance_endpoint_address
        rdsSql.connections.allow_default_port_from()

# app = core.App()
# RDSStack(app, "RDSStack")
# app.synth()