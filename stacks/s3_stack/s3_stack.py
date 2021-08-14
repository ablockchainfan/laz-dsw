from aws_cdk import core
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_kms as kms

class S3Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, key_arn: str, **kwargs) -> kms.Key:
        super().__init__(scope, id, **kwargs)

        # Create S3 buckets
        bucket = s3.Bucket(self, 'MyFirstBucket', 
            bucket_name='my-first-bucket',
            block_public_access=True,
            public_read_access=False,
            removal_policy=core.RemovalPolicy.DESTROY,
            encryption=s3.BucketEncryption.KMS,
            encryption_key=kms.Key.from_key_arn(key_arn),
            lifecycle_rules= [
                {
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
                }
            ]
        )