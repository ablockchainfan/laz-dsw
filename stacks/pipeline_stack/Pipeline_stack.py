from constructs import Construct
from stacks.KMS_stack.kms_stack import KmsStack
# from stacks.network_stack.network_stack import NetworkStack
from typing import Dict
# https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_codepipeline_actions/README.html
# https://github.com/aws-samples/aws-cdk-project-structure-python/blob/main/pipeline.py

from aws_cdk import Stage, Stack
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep

import aws_cdk.aws_codebuild as codebuild
from aws_cdk.aws_ecr import Repository
from utils.stack_util import add_tags_to_stack
import aws_cdk as core

class PipelineStack(Stack):

    def __init__(self, scope: Construct, id: str, config: Dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        pipeline = CodePipeline(self, "Pipeline",
                synth=ShellStep("Synth",
                    input=CodePipelineSource.connection("Kasarla1/laz-dsw", "main",
                    connection_arn="arn:aws:codestar-connections:us-east-1:222222222222:connection/7d2469ff-514a-4e4f-9003-5ca4a43cdc41"
                ),
                commands=["pip install -r requirements.txt", "npm install -g aws-cdk", "cdk synth"
                    ]
                )
            )
        env = core.Environment(account=config['awsAccount'],
                       region=config["awsRegion"],
                       )
        pipeline.add_stage(MyApplication(self, "Prod",
            env=env
        ))

class MyApplication(Stage):
    def __init__(self, scope, id, *, env=None, outdir=None):
        super().__init__(scope, id, env=env, outdir=outdir)

        # network_stack = NetworkStack(self,
        #                      "NetworkStack",
        #                      config=config,
        #                      env=env
        #                      )

        # print(network_stack.vpc.vpc_id)

        # security_stack = SecurityStack(app, 
        #                                 "SecurityStack", 
        #                                 vpc=network_stack.vpc,
        #                                 env = env
        #                             )

        kms_dev_lam = KmsStack(self, "kmsKeysStack2", env=env)