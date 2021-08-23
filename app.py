#!/usr/bin/env python3

from stacks.pipeline_stack.Pipeline_stack import MyApplication, PipelineStack
import sys
# from aws_cdk import core
from aws_cdk import App, Environment, Stack
# from aws_cdk.aws_ec2 import aws_ec2 as ec2
from aws_cdk.aws_codepipeline import Pipeline

from stacks.network_stack.network_stack import NetworkStack
from stacks.security_stack.security_stack import SecurityStack
from stacks.s3_stack.s3_stack import S3Stack

from stacks.compute_stack.compute_stack import ComputeStack
from stacks.data_stack.data_stack import DataStack
from stacks.KMS_stack.kms_stack import KmsStack
from utils import config_util

key_name = "id_rsa"  # Setup key_name for EC2 instance login 

app = App()

# Get target stage from cdk context
stage = app.node.try_get_context('stage')

print(stage)

if stage is None or stage == "unknown":
    sys.exit('You need to set the target stage.'
             ' USAGE: cdk <command> -c stage=dev <stack>')

# Load stage config and set cdk environment
config = config_util.load_config(stage)
env = Environment(account=config['awsAccount'],
                       region=config["awsRegion"],
                       )

# MyApplication(app,"myApp", env=env)
network_stack = NetworkStack(app,
                             "NetworkStack",
                             config=config,
                             env=env
                             )

print(network_stack.vpc.vpc_id)

# security_stack = SecurityStack(app, 
#                                 "SecurityStack", 
#                                 vpc=network_stack.vpc,
#                                 env = env
#                             )

kms_dev_lam = KmsStack(app, "kmsKeysStack", env=env)

compute_stack = ComputeStack(app,
                "ComputeStack",
                config=config,
                vpc=network_stack.vpc,
                sg_id=network_stack.es_sg_id, # security_stack.es_sg,
                env=env
             )



# create S3 stack
# apply IAM permissions to S3 resource ... (S3, principle, permissions)
# Allow Security group access input ( Src to Destination)?
data_stack = DataStack(app,
          "DataStack",
          config=config,
          vpc=network_stack.vpc,
          es_sg_id=network_stack.es_sg_id,
          kms_key = kms_dev_lam.key,
          env=env
          )

data_stack.rdsSql.connections.allow_default_port_from(network_stack.sg, "Allow access from Ec2 machines")
S3Stack(app,"s3Stack", kms_key=kms_dev_lam.key, env=env)

PipelineStack(app, "PipelineStack", config=config, env=env)

app.synth()
