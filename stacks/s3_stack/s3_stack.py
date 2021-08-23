from aws_cdk import Stack
from aws_cdk.aws_iam import Effect, PolicyStatement, ServicePrincipal
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_kms as kms
from constructs import Construct
import aws_cdk as core

class S3Stack(Stack):

    def __init__(self, scope: Construct, id: str, kms_key : kms.Key, **kwargs) -> kms.Key:
        super().__init__(scope, id, **kwargs)

        # Create S3 buckets
        bucket = s3.Bucket(self, 'MyFirstBucket', 
            bucket_name='my-first-bucket',
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            public_read_access=False,
            removal_policy=core.RemovalPolicy.DESTROY,
            encryption=s3.BucketEncryption.KMS,
            encryption_key=kms_key,
            lifecycle_rules= [
                    s3.LifecycleRule(
                        expiration=core.Duration.days(360),
                        transitions=[
                            s3.Transition(
                                storage_class=s3.StorageClass.INFREQUENT_ACCESS, 
                                transition_after=core.Duration.days(30)
                            ),
                            s3.Transition(
                                storage_class=s3.StorageClass.GLACIER, 
                                transition_after=core.Duration.days(90)
                            )
                        ]
                    )
            ]
        )
        
        # give the access to bucket from EC2
        bucket.add_to_resource_policy(PolicyStatement(
            actions=["s3:GetObject",
                     "s3:ListBucket",
                     "s3:PutBucketAcl"],
            effect=Effect.ALLOW,
            principals=[ServicePrincipal(service="ec2.amazonaws.com")],
            resources=['${bucket.bucket_arn}/*']
        ))