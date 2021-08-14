from aws_cdk import core
import aws_cdk.aws_kms as kms


class KmsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> kms.Key:
        super().__init__(scope, id, **kwargs)

        self.key = kms.Key(self, 'kms.db.lam.dev.aws', 
                removal_policy = core.RemovalPolicy.DESTROY,
                alias= 'alias/kms.db.lam.dev.aws',
                description= 'KMS key for encrypting the objects for dev LAM',
                enable_key_rotation= False,
            )