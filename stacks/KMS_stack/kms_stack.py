from aws_cdk import Stack
import aws_cdk as cdk
import aws_cdk.aws_kms as kms
import constructs


class KmsStack(Stack):

    def __init__(self, scope: constructs, id: str, **kwargs) -> kms.Key:
        super().__init__(scope, id, **kwargs)
        print("KMS Stack started")
        self.key = kms.Key(self, 'kms.db.lam.dev.aws', 
                removal_policy = cdk.RemovalPolicy.DESTROY,
                alias= 'alias/kms-db-lam-dev-aws',
                description= 'KMS key for encrypting the objects for dev LAM',
                enable_key_rotation= False,
            )